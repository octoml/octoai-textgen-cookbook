import os
import json
from typing import List
import base64

from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datasets import load_dataset
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
import openai
import requests

from enum import Enum


load_dotenv()



class ReviewCategory(Enum):
    ProductQuality = 'product quality'
    Packaging = 'packaging'
    Shipping = 'shipping'
    UnclearInstructions = 'unclear instructions'
    ContentQuality = 'content quality'
    SubscriptionAndBilling = 'subscription and billing'
    Other = 'other'


class JIRATicket(BaseModel):
    issue_title: str = Field("A short title explaining the core of the issue. Should be 8 words maximum.")
    issue_description: str = Field("A clear and descriptive explanation of what the issue is, what product does it relate to, how the customer is affected, and other relevant information.")
    is_urgent_reasoning: str = Field("An explanation whether the specific customer issue needs urgent fixing or not.")
    is_urgent: bool = Field("A true/false value indicating whether the issue needs urgent fixing or not. 'true' if it's urgent, 'false' otherwise")
    category: ReviewCategory = Field("What category is the given issue.")




FUNCTION_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "ask_for_more_information",
            "description": "Ask for more details regarding the review. Should be use to clarify what exactly is the issue, so that it's easier to fix it later.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reply_to_customer_review": {
                        "type": "string",
                        "description": "The text of the reply to the customer review, inquiring about more details regarding the complaint."
                    }
                },
                "required": ["reply_to_customer_review"]
            }
            # returns: Nothing, but we can simulate that it does recieve a reply from the user, just for this demo
        }
    },
    {
        "type": "function",
        "function": {
            "name": "say_thanks",
            "description": "Thank the user for the review they left. Should be used if the review is a positive one, with praise.",
            "parameters": {
                "type": "object",
                "properties": {
                    "thank_you_note": {
                        "type": "string",
                        "description": "The warm and welcoming 'Thank you' reply to the customer review."
                    }
                },
                "required": ["thank_you_note"]
            }
            # returns: Nothing
        }
    },
    {
        "type": "function",
        "function": {
            "name": "label_feedback_as_issue_and_apologize",
            "description": "Ask forgiveness from the user and assure them that the issue will be fixed. Should be used if the review is a negative one, or it's definitive that there's an issue, and it's very clear what the issue is.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product the issue is about."
                    },
                    "issue_description": {
                        "type": "string",
                        "description": "A short description of the customer issue."
                    },
                    "issue_category": {
                        "type": "enum", # TODO: ReviewCategory
                        "description": "What category is the given customer issue."
                    },
                    "sorry_note": {
                        "type": "string",
                        "description": "The warm and reassuring 'We are sorry' reply to the customer review."
                    }
                },
                "required": ["product_name", "issue_description", "issue_category", "sorry_note"]
            }
            # returns: Nothing
        }
    },
]


LLM_FUNCTIONS = {
    "label_feedback_as_issue_and_apologize": NotImplemented,
    "say_thanks": NotImplemented,
    "ask_for_more_information": NotImplemented
}


API_KEY = os.environ.get("OCTOAI_TOKEN")
NUM_PRODUCTS = int(os.environ.get("NUM_PRODUCTS", "5"))
MODEL = os.environ.get("MODEL_NAME", "meta-llama-3.1-8b-instruct")
SYSTEM_PROMPT = ("You are an helpful AI assistant helping a Senior Product Manager create user tickets for relevant issues."
                 " You must ensure that your call one of the provided functions, and only refer to the user feedback you received and nothing more.")

if MODEL not in ["meta-llama-3.1-405b-instruct",
                 "meta-llama-3.1-8b-instruct",
                 "meta-llama-3.1-70b-instruct"]:
    raise ValueError("The env var MODEL_NAME should be one of:",
                     ["meta-llama-3.1-405b-instruct",
                      "meta-llama-3.1-8b-instruct",
                      "meta-llama-3.1-70b-instruct"], "but got:", MODEL)

print("MODEL=", MODEL)
print("SYSTEM_PROMPT=", SYSTEM_PROMPT)



def process_review(client: openai.OpenAI, info: str, review: str):
    # NOTE: because it uses function calling, it may require multiple messages before returing
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Product Description:\n{info}\n========\nReview:\n{review}",
        },
    ]


    chat_completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.1,
        max_tokens=4096,
        tools=FUNCTION_DEFINITIONS,
        tool_choice="required",
    )

    agent_response = chat_completion.choices[0].message
    messages.append(
        {
            "role": agent_response.role,
            "content": "",
            "tool_calls": [
                tool_call.model_dump()
                for tool_call in chat_completion.choices[0].message.tool_calls
            ]
        }
    )

    tool_calls = chat_completion.choices[0].message.tool_calls

    while tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            # Call the function to get the response
            function_response = LLM_FUNCTIONS[function_name](**function_args)
            # Add the function response to the messages block
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        function_enriched_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=FUNCTION_DEFINITIONS,
            tool_choice="auto",
            temperature=0.1,
            max_tokens=4096,
        )

        agent_response = function_enriched_response.choices[0].message
        messages.append(
            {
                "role": agent_response.role,
                "content": "",
                "tool_calls": [
                    tool_call.model_dump()
                    for tool_call in function_enriched_response.choices[0].message.tool_calls
                ]
            }
        )

        tool_calls = function_enriched_response.choices[0].message.tool_calls

    return function_enriched_response.choices[0].message.content


def prepare_jira_ticket_info(client: openai.OpenAI, customer_issues: List[dict]):
    related_reviews = "\n========\n".join([f"Review:\nProduct Name: {issue['product_name']} (Category - {issue['category']})\n\nIssue:\n{issue['description']}" for issue in customer_issues])
    chat_completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "Important note, for the `issue_description` field, please summarize the following customer reviews according to the schema." + "\n\n" + related_reviews,
            },
        ],
        temperature=0.1,
        response_format={"type": "json_object", "schema": JIRATicket.model_json_schema()},
        max_tokens=4096,
    )
    try:
        response = json.loads(chat_completion.choices[0].message.content)
        return response
    except Exception:
        print("DEBUG >>>>", chat_completion)



def search_parent_asin(reviews, parent_asin):
    return [review for review in reviews if review["parent_asin"] == parent_asin]


def group_customer_issues(customer_issues, issue_embeddings):
    issue_embeddings_similarity = issue_embeddings.dot(issue_embeddings.T)
    square_mag = np.diag(issue_embeddings_similarity)

    # inverse squared magnitude
    inv_square_mag = 1 / square_mag

    # if it doesn't occur, set it's inverse magnitude to zero (instead of inf)
    inv_square_mag[np.isinf(inv_square_mag)] = 0

    # inverse of the magnitude
    inv_mag = np.sqrt(inv_square_mag)
        
    # cosine similarity (elementwise multiply by inverse magnitudes)
    cosine = issue_embeddings_similarity * inv_mag
    cosine_similarity = cosine.T * inv_mag

    # values on the diagonal should not interfere
    np.fill_diagonal(cosine_similarity, -1)


    distance_matrix = 1 - np.abs(cosine_similarity)
    linkage_matrix = linkage(distance_matrix, method='ward')
    threshold = 0.15
    clusters = fcluster(linkage_matrix, threshold, criterion='distance')


    grouped_customer_issues = []
    for unique_cluster_id in set(clusters):
        related_issues = [customer_issues[idx] for idx, cluster_id in enumerate(clusters) if cluster_id == unique_cluster_id]
        grouped_customer_issues.append(related_issues)
    return grouped_customer_issues


if __name__ == "__main__":
    client = openai.OpenAI(base_url="https://text.octoai.run/v1", api_key=API_KEY)

    # We use a dataset from Huggingface to quickly
    # see the performance on many examples
    dataset = load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023",
        "raw_meta_Magazine_Subscriptions",
        split="full",
        trust_remote_code=True,
    )
    reviews = load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023",
        "raw_review_Magazine_Subscriptions",
        split="full",
        trust_remote_code=True,
    )


    # 1: structure_customer_feedback
    customer_feedbacks = []
    for example in dataset.select(range(NUM_PRODUCTS)):
        long_description = example["title"] + "\n" + "".join(example["description"])
        product_reviews = search_parent_asin(reviews, example["parent_asin"])
        for review in product_reviews:
            customer_feedback = process_review(client, long_description, review["text"])
            customer_feedbacks.append(customer_feedback)


    print("products =", NUM_PRODUCTS, "issues =", len(customer_issues), "feedbacks =", len(customer_feedbacks))


    # 3: group by high similarity using GTE model from OctoAI
    issue_embeddings = []
    for issue in customer_issues:
        # NOTE: need to check context legnth of the model
        resp = client.embeddings.create(
            model="thenlper/gte-large",
            input=f"Product Name: {issue['product_name']} (Category - {issue['category']})\n\nIssue:\n{issue['description']}",
        )

        issue_embeddings.append(resp.data[0].embedding)

    issue_embeddings = np.array(issue_embeddings)

    grouped_customer_issues = group_customer_issues(customer_issues, issue_embeddings)


    # 4: Summarize the issue groups and make them into JIRA Tickets
    jira_tickets = []
    for issue_group in grouped_customer_issues:
        jira_ticket_info = prepare_jira_ticket_info(client, issue_group)
        jira_tickets.append(jira_ticket_info)

    print(jira_tickets)


    # 5: Send a REST request to JIRA server - mock
    is_mock = True
    if not is_mock:
        JIRA_PROJECT_KEY = ...
        JIRA_HOST = ...
        jira_email = ...
        generated_token = ...
        JIRA_API_KEY = base64.b64encode(f"{jira_email}:{generated_token}".encode()).decode()

        for ticket in jira_tickets:
            payload = {
                "fields": {
                    "project": {"key": JIRA_PROJECT_KEY},
                    "summary": ticket["issue_title"],
                    "description": ticket["issue_description"],
                    "issuetype": {
                        "name": "Bug"
                    },
                    "status": {
                        "name": "todo"
                    },
                    "priority": {
                        "name": "Highest" if ticket["is_urgent"] else "Normal"
                    },
                    # TODO: add the category label
                }
            }
            resp = requests.post(f"https://{JIRA_HOST}/rest/api/2/issue/", json=payload, headers={"Authentication": f"Basic {JIRA_API_KEY}", "Content-Type": "application/json"})
            resp.raise_on_status()


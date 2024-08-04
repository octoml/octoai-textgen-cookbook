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


API_KEY = os.environ.get("OCTOAI_TOKEN")
NUM_PRODUCTS = int(os.environ.get("NUM_PRODUCTS", "5"))
FUNCTION_MODEL = os.environ.get("FUNCTION_MODEL_NAME", "meta-llama-3.1-8b-instruct")
JSON_MODEL = "meta-llama-3-8b-instruct"
SYSTEM_PROMPT = ("You are an helpful AI assistant helping a Senior Customer Success Manager interact with users and create user tickets for relevant issues."
                 " You must ensure that you call one of the provided functions if necessary, and only refer to the user feedback you received and nothing more."
                 " You can ask for clarifications multiple times, but thanking the user or asking forgiveness should be done just once.")

if FUNCTION_MODEL not in ["meta-llama-3.1-8b-instruct",
                          "meta-llama-3.1-405b-instruct",
                          "meta-llama-3.1-70b-instruct"]:
    raise ValueError("The env var FUNCTION_MODEL_NAME should be one of:",
                     ["meta-llama-3.1-8b-instruct",
                      "meta-llama-3.1-405b-instruct",
                      "meta-llama-3.1-70b-instruct"], "but got:", FUNCTION_MODEL)

print("FUNCTION_MODEL =", FUNCTION_MODEL)
print("JSON_MODEL =", JSON_MODEL)
print("SYSTEM_PROMPT =", SYSTEM_PROMPT)

CUSTOMER_ISSUES_REGISTRY = []


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
            "description": "Ask for more details regarding the review. Should be used to clarify what exactly is the issue, so that it's easier to fix it later. This function can be called multiple times.",
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
            # NOTE: Normally this should return nothing, but we can simulate that it does recieve a reply from the user, just for this demo
        }
    },
    {
        "type": "function",
        "function": {
            "name": "say_thanks",
            "description": "Thank the user for the review they left. Should be used if the review is a positive one, with praise. This function must never be called more than once.",
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "label_feedback_as_issue_and_apologize",
            "description": "Ask forgiveness from the user and assure them that the issue will be fixed. Should be used if the review is a negative one, or it's definitive that there's an issue, and it's very clear what the issue is. This function must never be called more than once.",
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
                        "type": "string",
                        "enum": [category.value for category in ReviewCategory],
                        "description": "What category is the given customer issue."
                    },
                    "sorry_note": {
                        "type": "string",
                        "description": "The warm and reassuring 'We are sorry' reply to the customer review."
                    }
                },
                "required": ["product_name", "issue_description", "issue_category", "sorry_note"]
            }
        }
    },
]


print(FUNCTION_DEFINITIONS)


def ask_for_more_information(reply_to_customer_review: str, **kwargs) -> dict:
    """In a real-world implementation this will need to actually reply to the user feedback, possibly via a REST API"""
    feedback_content = kwargs.get("feedback_content", "")
    product_info = kwargs.get("product_info", "")

    messages = [
        {"role": "system", "content": "Assume that you're a customer who left a product review. Be helpful and cooperate with the customer success manager two find a solution."},
        {
            "role": "user",
            "content": f"For some context. Given this product description:\n{product_info}\n\n And this review that you left:\n{feedback_content}\n\nThe representative of the product replied to your feedback:\n\n{reply_to_customer_review}\n\nPlease answer them.",
        },
    ]

    chat_completion = client.chat.completions.create(
        model=JSON_MODEL,
        messages=messages,
        temperature=0.1,
        max_tokens=4096
    )

    return {"user_reply": chat_completion.choices[0].message.content}


def say_thanks(thank_you_note: str, **kwargs) -> dict:
    """In a real-world implementation this will need to actually reply to the user feedback, possibly via a REST API"""
    print(">>> Called say_thanks")
    return {"status": "submitted successfully"}


def label_feedback_as_issue_and_apologize(product_name: str, issue_description: str, issue_category: str, sorry_note: str, **kwargs) -> dict:
    """In a real-world implementation this will need to actually reply to the user feedback, possibly via a REST API"""
    global CUSTOMER_ISSUES_REGISTRY
    CUSTOMER_ISSUES_REGISTRY.append({"product_name": product_name, "category": issue_category, "description": issue_description})
    print(">>> Called label_feedback_as_issue_and_apologize")
    return {"status": "submitted successfully"}


LLM_FUNCTIONS = {
    "label_feedback_as_issue_and_apologize": label_feedback_as_issue_and_apologize,
    "say_thanks": say_thanks,
    "ask_for_more_information": ask_for_more_information,
    # NOTE: you can even implement a RAG-function using the products' documentation, to let the agent answer some of the users' questions
}


def process_review(client: openai.OpenAI, product_info: str, feedback_content: str):
    # NOTE: because it uses function calling, it may require multiple messages before returing
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Product Description:\n{product_info}\n========\nReview:\n{feedback_content}",
        },
    ]

    chat_completion = client.chat.completions.create(
        model=FUNCTION_MODEL,
        messages=messages,
        temperature=0.1,
        max_tokens=4096,
        tools=FUNCTION_DEFINITIONS,
        tool_choice="auto",
    )

    agent_response = chat_completion.choices[0].message
    if not agent_response.tool_calls:
        return

    messages.append(
        {
            "role": agent_response.role,
            "content": "",
            "tool_calls": [
                tool_call.model_dump()
                for tool_call in agent_response.tool_calls
            ]
        }
    )

    tool_calls = agent_response.tool_calls

    abort_counter = 3
    while abort_counter > 0:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            # Call the function to get the response
            function_response = LLM_FUNCTIONS[function_name](feedback_content=feedback_content, product_info=product_info, **function_args)
            # Add the function response to the messages block
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )

        function_enriched_response = client.chat.completions.create(
            model=FUNCTION_MODEL,
            messages=messages,
            tools=FUNCTION_DEFINITIONS,
            tool_choice="auto",
            temperature=0.2,
            max_tokens=4096,
        )

        agent_response = function_enriched_response.choices[0].message
        if not agent_response.tool_calls:
            break
        else:
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

            abort_counter -= 1

    return function_enriched_response.choices[0].message.content


def prepare_jira_ticket_info(client: openai.OpenAI, customer_issues: List[dict]):
    related_reviews = "\n========\n".join([f"Review:\nProduct Name: {issue['product_name']} (Category - {issue['category']})\n\nIssue:\n{issue['description']}" for issue in customer_issues])
    chat_completion = client.chat.completions.create(
        model=JSON_MODEL,
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


    print("products =", NUM_PRODUCTS, "issues =", len(CUSTOMER_ISSUES_REGISTRY), "feedbacks =", len(customer_feedbacks))


    # 3: group by high similarity using GTE model from OctoAI
    issue_embeddings = []
    for issue in CUSTOMER_ISSUES_REGISTRY:
        # NOTE: need to check context legnth of the model
        resp = client.embeddings.create(
            model="thenlper/gte-large",
            input=f"Product Name: {issue['product_name']} (Category - {issue['category']})\n\nIssue:\n{issue['description']}",
        )

        issue_embeddings.append(resp.data[0].embedding)

    issue_embeddings = np.array(issue_embeddings)

    grouped_customer_issues = group_customer_issues(CUSTOMER_ISSUES_REGISTRY, issue_embeddings)


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


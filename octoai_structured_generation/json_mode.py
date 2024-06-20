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

from benchmark import Benchmark


load_dotenv()


API_KEY = os.environ.get("OCTOAI_TOKEN")
SAVE_TO_FILE = os.environ.get("SAVE_BENCHMARK_RESULTS")
NUM_PRODUCTS = int(os.environ.get("NUM_PRODUCTS", "5"))
MODEL = os.environ.get("MODEL_NAME", "mistral-7b-instruct")
SYSTEM_PROMPT = ("You are an helpful AI assistant helping a Senior Product Manager create user tickets for relevant issues."
                 " You must ensure that your responses only refer to the user feedback you received and nothing more.")

if MODEL not in ["mistral-7b-instruct",
                 "mixtral-8x7b-instruct",
                 "meta-llama-3-8b-instruct",
                 "meta-llama-3-70b-instruct"]:
    raise ValueError("The env var MODEL_NAME should be one of:", ["mistral-7b-instruct",
                 "mixtral-8x7b-instruct",
                 "meta-llama-3-8b-instruct",
                 "meta-llama-3-70b-instruct"], "but got:", MODEL)

print("MODEL=", MODEL)
print("SYSTEM_PROMPT=", SYSTEM_PROMPT)


class CustomerFeedback(BaseModel):
    description: str = Field(
        description="A short description of the customer feedback."
    )
    product_name: str = Field("The name of the product the feedback is about.")
    # NOTE: that's basically structured CoT prompting, amazing right?
    is_issue_reasoning: str = Field("An explanation whether the specific customer feedback should be treated as a problem/issue, or a positive comment.")
    is_issue: bool = Field("A true/false value indicating whether the specific customer feedback is a problem/issue, or a positive comment. Must be 'true' if it's an issue, and 'false' otherwise")
    category: str = Field("What category is the given customer feedback. It should be one of the following: 'product-quality', 'packaging', 'shipping', 'unclear-instructions', 'content-quality', 'subscription-and-billing', 'other'. Make the category is all lowercase, and whitespace is replaced with a dash ('-').")


class JIRATicket(BaseModel):
    issue_title: str = Field("A short title explaining the core of the issue. Should be 8 words maximum.")
    issue_description: str = Field("A clear and descriptive explanation of what the issue is, what product does it relate to, how the customer is affected, and other relevant information.")
    is_urgent_reasoning: str = Field("An explanation whether the specific customer issue needs urgent fixing or not.")
    is_urgent: bool = Field("A true/false value indicating whether the issue needs urgent fixing or not. 'true' if it's urgent, 'false' otherwise")
    category: str = Field("What category is the given customer issue. It should be one of the following: 'product-quality', 'packaging', 'shipping', 'unclear-instructions', 'content-quality', 'subscription-and-billing', 'other'. Make the category is all lowercase, and whitespace is replaced with a dash ('-').")


def structure_customer_feedback(client: openai.OpenAI, info: str, review: str, benchmark_client: Benchmark):
    run_id = benchmark_client.new_run()
    chat_completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Product Description:\n{info}\n========\nReview:\n{review}",
            },
        ],
        temperature=0.1,
        max_tokens=4096,
        response_format={"type": "json_object", "schema": CustomerFeedback.model_json_schema()},
    )
    benchmark_client.add_input_tokens(run_id, chat_completion.usage)
    try:
        response = json.loads(chat_completion.choices[0].message.content)
        benchmark_client.end(run_id)
        return response
    except Exception:
        benchmark_client.end_with_error(run_id)
        print("DEBUG >>>>", chat_completion)


def prepare_jira_ticket_info(client: openai.OpenAI, customer_issues: List[CustomerFeedback], benchmark_client: Benchmark):
    run_id = benchmark_client.new_run()
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
    benchmark_client.add_input_tokens(run_id, chat_completion.usage)
    try:
        response = json.loads(chat_completion.choices[0].message.content)
        benchmark_client.end(run_id)
        return response
    except Exception:
        benchmark_client.end_with_error(run_id)
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

    benchmark_client = Benchmark()


    # 1: structure_customer_feedback
    customer_feedbacks = []
    for example in dataset.select(range(NUM_PRODUCTS)):
        long_description = example["title"] + "\n" + "".join(example["description"])
        product_reviews = search_parent_asin(reviews, example["parent_asin"])
        for review in product_reviews:
            customer_feedback = structure_customer_feedback(client, long_description, review["text"], benchmark_client)
            customer_feedbacks.append(customer_feedback)


    # 2: filter only is_issue
    customer_issues = []
    for feedback in customer_feedbacks:
        try:
            if feedback["is_issue"]:
                customer_issues.append(feedback)
        except Exception as ex:
            print(ex, "got this error with feedback =", feedback, "... moving on")
            continue

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
        jira_ticket_info = prepare_jira_ticket_info(client, issue_group, benchmark_client)
        jira_tickets.append(jira_ticket_info)

    print(jira_tickets)

    benchmark_client.print_summary(save_to_file=SAVE_TO_FILE)


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


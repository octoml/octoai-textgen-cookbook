import os
from pydantic import BaseModel, Field
from typing import List
from load_dotenv import load_dotenv

from datasets import load_dataset

import openai

load_dotenv()

api_key = os.environ["OCTOAI_TOKEN"]
model = "mixtral-8x7b-instruct"

SYSTEM_PROMPT = "You are a world class marketer a product reviewver. Every input text you receive you will have a long description with some information about a product and separately some reviews of the product. Your job is to generate a list of short product cards. Each card has two elements: a short description, and a title. Generate the title and description based on the language provided in the designator, that can be English, French, Italian, German, or Spanish. Also, append a list of pros and cons of the product, only based on the reviews. The list of pros and cons should not be longer than 3 elements."


class Description(BaseModel):
    description: str = Field(
        description="Short description of the product, a summary given certain information, in the given language."
    )
    title: str = Field(
        description="Short title of the product, no more than a couple of words, in the given language."
    )


class Product(BaseModel):
    english: Description = Field(
        description="Short description of the product in English"
    )
    french: Description = Field(
        description="Short description of the product in French"
    )
    italian: Description = Field(
        description="Short description of the product in Italian"
    )
    german: Description = Field(
        description="Short description of the product in German"
    )
    spanish: Description = Field(
        description="Short description of the product in Spanish"
    )
    pros: List[str] = Field(
        description="List of benefits and advantages of the product",
        max_length=3,
    )
    cons: List[str] = Field(
        description="List of drawbacks and disadvantages of the product",
        max_length=3,
    )


def generate_descriptions(client: openai.OpenAI, info: str, reviews: str):
    """
    This function calls the OctoAI API using OpenAI's Python client to generate
    structured data given an input text.

    We define the system prompt inside the function.
    """
    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Information:\n{info}\n========\nReviews:\n{reviews}",
            },
        ],
        temperature=0,
        response_format={"type": "json_object", "schema": Product.model_json_schema()},
    )
    return chat_completion.choices[0].message.content


def search_parent_asin(reviews, parent_asin):
    return [review for review in reviews if review["parent_asin"] == parent_asin]


if __name__ == "__main__":
    client = openai.OpenAI(base_url="https://text.octoai.run/v1", api_key=api_key)

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
    for example in dataset.select(range(1)):
        long_description = example["title"] + "\n" + "".join(example["description"])
        reviews = search_parent_asin(reviews, example["parent_asin"])
        long_reviews = "\n".join([review["text"] for review in reviews])
        print(generate_descriptions(client, long_description, long_reviews))

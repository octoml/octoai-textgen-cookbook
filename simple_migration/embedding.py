from openai import OpenAI
import os

client = OpenAI(
   base_url = "https://text.octoai.run/v1",
   api_key = os.environ['OCTOAI_TOKEN']
)

response = client.embeddings.create(
    # model="text-embedding-ada-002",
    model="thenlper/gte-large",
    input=[
        "The food was delicious and the waiter...",
    ],
)

print(response)

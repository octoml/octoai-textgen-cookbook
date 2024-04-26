from os import environ
from llama_index.llms.octoai import OctoAI

OCTOAI_API_KEY = environ.get("OCTOAI_TOKEN")

octoai = OctoAI(model="meta-llama-3-8b-instruct", token=OCTOAI_API_KEY)

# Using complete
response = octoai.complete("Octopi can not play chess because...")
print(response)

print("\n=====================\n")

# Using the chat interface
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system",
        content="Below is an instruction that describes a task. Write a response that appropriately completes the request.",
    ),
    ChatMessage(role="user", content="Write a short blog about Seattle"),
]
response = octoai.chat(messages)
print(response)

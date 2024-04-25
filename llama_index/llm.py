from llama_index.llms.octoai import OctoAI
from os import environ

OCTOAI_API_KEY = environ.get("OCTOAI_TOKEN")
octoai = OctoAI(model="llama-2-13b-chat", token=OCTOAI_API_KEY)
response = octoai.complete("Octopi can not play chess because...")
print(response)

import os


# llama_index
from llama_index.llms.openai_like import OpenAILike
from llama_index.core.agent import ReActAgent

# tools
from tools.guidelines import guidelines_engine
from tools.web_reader import web_reader_engine
from tools.report_generator import report_generator

from os import environ

llm = OpenAILike(
    model="meta-llama-3.1-70b-instruct",
    api_base="https://text.octoai.run/v1",
    api_key=environ["OCTOAI_API_KEY"],
    context_window=40000,
    is_function_calling_model=True,
    is_chat_model=True,
)

agent = ReActAgent.from_tools(
    tools=[
        guidelines_engine,  # <---
        web_reader_engine,  # <---
        report_generator,  # <---
    ],
    llm=llm,
    verbose=True,
)

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = agent.chat(user_input)
print("Agent: ", response)

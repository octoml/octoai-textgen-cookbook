import os
import arize_otel

# Import open-telemetry dependencies
from arize_otel import register_otel, Endpoints

# Setup OTEL via our convenience function
register_otel(
    endpoints=Endpoints.ARIZE,
    space_key="137deb0",  # in app Space settings page
    api_key="5cb9e48c89bdcd3438b",
    model_id="llamaindex-agent",
)
# Import the automatic instrumentor from OpenInference
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

# Finish automatic instrumentation
LlamaIndexInstrumentor().instrument()


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

# response = llm.complete("Hello World!")
# print(str(response))

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

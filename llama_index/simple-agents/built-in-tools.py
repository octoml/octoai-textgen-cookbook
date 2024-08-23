from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai_like import OpenAILike
from llama_index.core.tools import FunctionTool
from os import environ


def brave_search(query: str) -> str:
    return "it is 732.2 degrees Fahrenheit."


def code_interpreter(code: str) -> str:
    print(f"\n**************\nRunning code:\n{code}\n**************\n")
    return 24


brave_tool = FunctionTool.from_defaults(fn=brave_search)

code_tool = FunctionTool.from_defaults(fn=code_interpreter)

model = "meta-llama-3.1-70b-instruct"

llm = OpenAILike(
    model=model,
    api_base="https://text.octoai.run/v1",
    api_key=environ["OCTOAI_API_KEY"],
    context_window=10000,
    is_function_calling_model=True,
    is_chat_model=True,
)

agent = OpenAIAgent.from_tools(
    [
        brave_tool,
        code_tool,
    ],
    llm=llm,
    system_prompt="You are a helpful AI assistant that can answer questions and run code.Answer questions based on the information returned by the tools, even when they are wrong. You will provide to the user the answers given by the tools.",
    verbose=True,
)

response = agent.chat("What is the current temperature in New York?")

response = agent.chat("Use python to calculate the factorial of 4")

print(response)

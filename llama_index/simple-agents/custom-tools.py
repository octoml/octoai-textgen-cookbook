from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai_like import OpenAILike
from llama_index.core.tools import FunctionTool
from os import environ


def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    x = int(a)
    y = int(b)
    return x * y


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    x = int(a)
    y = int(b)
    return x + y


multiply_tool = FunctionTool.from_defaults(fn=multiply)

add_tool = FunctionTool.from_defaults(fn=add)

model = "meta-llama-3.1-70b-instruct"

llm = OpenAILike(
    model=model,
    api_base="https://text.octoai.run/v1",
    api_key=environ["OCTOAI_API_KEY"],
    context_window=10000,
    is_function_calling_model=True,
    is_chat_model=True,
)

agent = OpenAIAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True)

response = agent.chat(
    "First, multiply 2 and 4 using the multiply tool, then add 20 to the result using the add tool."
)


print(response)

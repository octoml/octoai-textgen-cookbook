import os
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.pydantic_v1 import BaseModel, Field


class FlightNumber(BaseModel):
    query: str = Field(description="The flight number, e.g., AA100")


class Date(BaseModel):
    query: str = Field(description="The date of the flight, e.g., 2024-06-17")


@tool
def get_flight_status(flight_number: FlightNumber, date: Date):
    """
    Get the current status of a flight
    """
    print("Executing function: Getting flight status")
    return f"The flight {flight_number} on {date} is on time."


@tool
def get_current_date():
    """
    Gets the current date
    """
    print("Executing function: Getting current date")
    return "2024-06-17"


tools = [get_flight_status, get_current_date]

# llm = ChatOpenAI(
#     model_name="meta-llama-3.1-70b-instruct",
#     openai_api_key=os.environ["OCTOAI_API_TOKEN"],
#     openai_api_base="https://text.octoai.run/v1",
#     temperature=0.4,
#     max_tokens=10000,
# )

llm = ChatOpenAI()

from langgraph.prebuilt import create_react_agent

system_prompt = "You are a helpful bot named Fred. You have access to two tools: one that gets the current date and another that gets the status of a flight. Provide short answers to the user's questions."
graph = create_react_agent(llm, tools=tools, state_modifier=system_prompt)
inputs = {"messages": [("user", "what is the status of flight AA100?")]}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()

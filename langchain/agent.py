import os
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
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
    return f"The flight {flight_number} on {date} is on time."


tools = [get_flight_status]

model = ChatOpenAI(
    model="meta-llama-3-70b-instruct",
    openai_api_key=os.environ["OCTOAI_API_TOKEN"],
    openai_api_base="https://text.octoai.run/v1",
)

agent_executor = create_react_agent(model, tools)

response = agent_executor.invoke(
    {"messages": [HumanMessage(content="What is the status of flight AA100?")]}
)

for message in response["messages"]:
    print(message)

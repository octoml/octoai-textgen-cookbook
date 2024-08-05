import os
from langchain_openai import ChatOpenAI

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_flight_status",
            "description": "Get the current status of a flight",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {
                        "type": "string",
                        "description": "The flight number, e.g., AA100",
                    },
                    "date": {
                        "type": "string",
                        "format": "date",
                        "description": "The date of the flight, e.g., 2024-06-17",
                    },
                },
                "required": ["flight_number", "date"],
            },
        },
    }
]

model = ChatOpenAI(
    model="mistral-7b-instruct",
    openai_api_key=os.environ["OCTOAI_API_KEY"],
    openai_api_base="https://text.octoai.run/v1",
).bind(tools=tools)


message = model.invoke(
    "I have a flight booked for tomorrow with American Airlines, flight number AA100. Can you check its status for me?"
)

print(message.tool_calls)

# It should print the following:
# [{'name': 'get_flight_status', 'args': {'flight_number': 'AA100', 'date': '2024-06-18'}, 'id': 'call_7aQI3oC5ZXYIErUmbB05EkDH'}]

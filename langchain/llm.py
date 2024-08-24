# Set your api key via the OCTOAI_API_TOKEN environment variable
from langchain_community.chat_models.octoai import ChatOctoAI


llm = ChatOctoAI(
    model_name="meta-llama-3.1-70b-instruct",
    max_tokens=10000,
    temperature=0.4,
    model_kwargs={},
)

messages = [
    (
        "system",
        "You are a helpful assistant. Provide short answers to the user's questions.",
    ),
    ("human", "Who was Leonardo DaVinci?"),
]
ai_msg = llm.invoke(messages)

print(ai_msg.content)

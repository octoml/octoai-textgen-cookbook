from openai import OpenAI
import os

client = OpenAI(
   base_url = "https://text.octoai.run/v1",
   api_key = os.environ['OCTOAI_TOKEN']
)

completion = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    model="llama-2-13b-chat-fp16",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)

print(completion.choices[0].message)

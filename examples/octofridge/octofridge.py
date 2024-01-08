import os
from octoai.client import Client

octoai_token = os.environ.get('OCTOAI_API_TOKEN')

print("Welcome to OctoFridge!")
ingredients = input("Enter the ingredients in your fridge in a comma separated list and hit <enter> : ")

def textgen(model_name, \
            prompt, \
            role = "user", \
            temperature = 1.0, \
            top_p = 1.0, \
            stream = False, \
            max_tokens = 1024, \
            presence_penalty = 0.0, \
            frequency_penalty = 0.0):

    client = Client(token=octoai_token)
    completion = client.chat.completions.create(
        model = model_name,
        messages = [
        {
            "role": role,
            "content": prompt
        }
        ],
        temperature = temperature,
        top_p = top_p,
        stream = stream,
        max_tokens = max_tokens,
        presence_penalty = presence_penalty,
        frequency_penalty = frequency_penalty
    )

    # return message
    return completion.choices[0].message.content

model_name = "llama-2-13b-chat-fp16"    
recipe = textgen(model_name, f"Please create a recipe using the following ingredients: {ingredients}")
print(recipe)

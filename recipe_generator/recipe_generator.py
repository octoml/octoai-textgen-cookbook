from octoai.client import Client


def textgen(model_name,
            prompt,
            role = "user",
            temperature = 1.0,
            top_p = 1.0,
            stream = False,
            max_tokens = 1024,
            presence_penalty = 0.0,
            frequency_penalty = 0.0):

    client = Client()
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


if __name__ == "__main__":
    # This code is used to interactively ask for a list of comma-separated ingredients.
    # It uses the OctoAI-hosted large language model to generate a recipe.
    print("Welcome to OctoFridge!")
    ingredients = input("Enter the ingredients in your fridge in a comma separated list and hit <enter> : ")

    recipe = textgen(
        "llama-2-13b-chat-fp16",
        f"Please create a recipe using the following ingredients: {ingredients}"
    )
    print("\n{}".format(recipe))

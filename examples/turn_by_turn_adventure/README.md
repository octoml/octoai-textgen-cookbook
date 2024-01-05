# Turn by Turn adventure

A very basic chat bot using Langchain and OctoAI LLM (here we're using LLAMA2 70b chat)

## Instructions

- Set up python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install the pip requirements in your local python virtual environment

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```
### Environment setup

To run our example app, there are two simple steps to take:

- Get an OctoAI API token by following [these instructions](https://docs.octoai.cloud/docs/how-to-create-an-octoai-access-token).
- Paste your API token in the file called `.env` in this directory.

```bash
OCTOAI_API_TOKEN=<your key here>
```

- Run `chat.py` script to chat with the LLM hosted endpoint.
```bash
python3 chat.py
```

- Example usage:

```
Prompt: what is the capital of washington state
Response(1.5 sec):   The capital of Washington state is Olympia.

Prompt: how do you fry an egg
Response(8.9 sec):   Sure! Here's a step-by-step guide on how to fry an egg:

1. Crack an egg into a non-stick pan or skillet over medium heat.
2. Let the egg cook for about 2-3 minutes or until the whites are set and the yolks are cooked to your desired doneness.
3. Use a spatula to carefully flip the egg over and cook for another 30 seconds to 1 minute on the other side.
4. Remove the egg from the pan and serve immediately.

Here are a few tips to help you achieve the perfect fried egg:

* Use a non-stick pan to prevent the egg from sticking and to make it easier to flip.
* Adjust the heat as needed to prevent the egg from cooking too quickly or too slowly.
* Don't overcrowd the pan. Fry eggs one at a time to ensure they cook evenly.
```
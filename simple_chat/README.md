# How to build a simple chat bot with OctoAI and Langchain in Python

OctoAI LLMs such as Llama2-70b are very capable open source large language models (LLMs) that can be used to power your chat apps (e.g. a Q&A bot like the one we'll demonstrate here).

In this example, you will build a dead-simple Python app powered by a Llama2-70b hosted on OctoAI, and Langchain. The app runs on your terminal, all you need is a python interpreter, and you're ready to install the dependencies and get going!

## What you will build

This simple chat app is really the "hello world" of chat apps that you can build with Langchain. This app is great if you're a Python programmer, are just getting started with building your very first LLM app, and want a taste of the amazing benefits that open source LLMs on OctoAI present (customizability, control, ease of management, performance, scalability, costs etc.).

We intentionally stripped a lot of complexity away in this example to give you a barebones Q&A bot that you can play with and ultimately extend for your own needs.

All the app does is listen for a user prompt that gets entered via keyboard. Based on the promp, it'll rely on OctoAI's Llama2-70b to answer based on the pre-trained knowledge. We're not connecting the model to, say a vector data base to augment its knowledge here (we'll learn how to do this in other cookbook examples).

In addition the LLM chain is devoid of memory - this means that if you ask two back to back questions where the second question relies on context from the first question (e.g. what country is Berlin in; list the neighboring countries), the LLM won't be able to answer the second question based on that first question/answer context. This is intentional as our aim here is to build a very simple bot! So each question should be asked as if you were starting a brand new conversation!

## What you will use

The key to using OctoAI open source LLMs successfully in this Lanchain python app is to do the following:

1. First import the OctoAI endpoint in Langchain via these two lines:

```python
from langchain.llms.octoai_endpoint import OctoAIEndpoint
```

You've probably been exposed to other LLM providers like OpenAI or Antropic; the idea with this line is that you can import the OctoAI LLM endpoint as a drop-in replacement to other LLM endpoints you might have used in the past!

2. To instantiate the OctoAI LLM that you'll be using to power your chain, you have to add the lines below:

```python
llm = OctoAIEndpoint(
    endpoint_url="https://text.octoai.run/v1/chat/completions",
    model_kwargs={
        "model": "llama-2-70b-chat-fp16",
        "messages": [
            {
                "role": "system",
                "content": "Below is an instruction that describes a task. Write a response that appropriately completes the request.",
            }
        ],
        "stream": False,
        "max_tokens": 256,
    },
)
```

All we're doing here is: set the model to be Llama2-70b-chat (there are many other flavors of open source LLMs available on OctoAI that we invite you all to try out!), define the behavior of the LLM, and finally indicate that streaming mode is turned off, and that we'll cap output tokens at 256 to keep answers concise.

3. Set up the language model chain. From here on end it's all smooth sailing if you've used Langchain before. Initialize your language model chain and you're good to go!

```python
# Set up the language model chain
llm_chain = LLMChain(prompt=prompt, llm=llm)
```

The prompt here refers to the string in which we've stored the user keyboard input.

Voila! With this bare-bones example you're ready to start building exciting LLM applications with Langchain and OctoAI!

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

- Get an OctoAI API token by following [these instructions](https://octo.ai/docs/getting-started/how-to-create-octoai-api-token/).
- Paste your API token in the file called `.env` in this directory.

```bash
OCTOAI_API_TOKEN=<your key here>
```

### Running the application

Run `chat.py` script to chat with the LLM hosted endpoint.
```bash
python3 chat.py
```

### Example usage

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

## License

This project is licensed under the MIT License.

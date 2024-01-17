# How to build a turn by turn adventure game with OctoAI and Langchain in Python

Mixture of Experts models like Mixtral-8x7b are pushing the boundaries on what open source large language models (LLMs) can achieve, like the turn by turn adventure game we'll be showcasing in this app.

In this example, you will build a simple yet effective turn by turn adventure game powered by Mixtral-8x7b hosted on OctoAI, and Langchain. The app runs on your terminal, all you need is a python interpreter, and you're ready to install the dependencies and get going!

## Acknowlegements

This example was heavily inspired by the choose your own adventure game example written by Tech With Tim: https://github.com/techwithtim/AI-Choose-Your-Own-Adventure-Game.

## What you will build

This turn by turn adventure game extend very basic Langchain app like the `simple_chat` app by introducing (1) prompt template engineering, (2) memory, and (3) a very capable open source model, Mixtral-8x7b that rivals in capabilities some of the proprietary LLMs.

This app is great if you're a Python programmer, have just built your very first LLM app and want to take it up a notch in levels of fun and complexity!

If you've ever tried to code up a turn by turn adventure game you'll appreciate how hard it can get due to the exponential growth in story paths at every turn of the adventure! It quickly becomes intractable. With LLMs we can code up a turn by turn adventure game in just a 100 lines of code!

More impressive is that you can create whole new adventure stories and scenarios by editing just a couple of lines of code! For instance we've created this adventure game to be about being part of the first mission that will land on Mars. But in just a few lines of code you can change the setting and goals to be set in some fantasy world! Or any other setting your heart desires.

## What you will use

The key to using OctoAI open source LLMs successfully in this Lanchain python app is to take advantage the following:

### 1. Prompt template engineering
Here, we are instructing our LLMs how to conduct/narrate the adventure and we're mainly setting the context and story for the adventure. For instance you can edit the first two lines to set your adventure anywhere you want!

```text
You are now the guide of a turn by turn adventure set on earth, in the year 2050.
The objective for the player of this adventure is to successfully land on planet Mars.
You must navigate them through challenges, choices, and consequences,
dynamically adapting the story based on the player's decisions.
Your goal is to create a branching narrative experience where each choice
leads to a new path, ultimately determining the player's fate.
```

We can codify additional rules to more tightly control the behavior of the LLM model. For instance instruct the LLM to only ever give the player 3 choices when they decide what to do next. Or define how the game should start and end.

```text
Here are some rules to follow at all costs:
1. Be concise, wait at every turn for me to provide a human prompt
2. On the first turn, let the player chose one of 3 character classes
3. Always present the player 3 choices labeled A, B and C
4. Have a few paths that lead to success
5. Have some paths that lead to mission failure: in that case, conclude the text with: "The End.", I will search for this text to end the game
6. Reach success or failure after 3 turns
```

Note how natural these instructions are! They are as intelligible to a human as they are to an LLM! It's worth pausing here and appreciating how far we've gone: we can now program machines the same way we "program" humans: by just talking to them and giving them clear instructions instead of writing code!

Be aware that to get the best experience you'll need to tweak this prompt a bit, especially if you use different models as drop-in subsitutes to Mixtral-8x7b. The intent here is to give you a starting point so you can refine your adventure!

### 2. Memory
With memory you're providing history on prior conversations to your LLM as they narrate every new step in the adventure. This is a key concept to make your LLM chain work - without memory you can't go very far in a turn by turn adventure!

The way we make use of memory in langchain is straigthforard. You'll need to instantiate a conversation buffer. According to the [langchain documentation](https://python.langchain.com/docs/modules/memory/types/buffer): this memory allows for storing messages and then extracts the messages in a variable.


```python
chat_history = ConversationBufferMemory(memory_key="chat_history")
```

Then in your prompt template you'll need to add context, as follows:

```text
Here is the chat history, use this to understand what to say next: {chat_history}
```

Finally when instantiating the langchain `PromptTemplate`, you'll need to add `chat_history` to your `input_variables` list.

And when you instantiate your chain, you'll pass in the conversational buffer alongside your prompt and the OctoAI LLM, as follows:
```
llm_chain = LLMChain(
    prompt=prompt,
    llm=llm,
    memory=chat_history
)
```

### 3. Mixtral-8x7b
As of the time of this writing, Mixtral-8x7b is one of the more exciting and capable open source models out there [source](https://arxiv.org/abs/2401.04088). It's an instance of a Sparse Mixture of Experts (SMoE) language model.

Mixtral is based on the architecture as Mistral-7b, with the difference that each layer is composed of 8 "experts". Based on the tokens that are coming in, a router network selects two experts to process the current state and combine their outputs. What does it mean? You're basically using a very polyvalent model that excels at mathematics, code generation, and multilingual benchmarks on top of being a very agreeable chat model!

Note that we can instantiate a Mixtral model pretty easily with the OctoAI LLM endpoint by defining the model entry in the `model_kwargs` to be `mixtral-8x7b-instruct-fp16`.

Another note: we're not using all of the amazing Mixture of Experts capabilities offered by Mixtral here - mainly we're using the LLM as a chat bot. But it's fine! We'll explore ways to explore all of the goodness that SMoE language models offer in other examples!

```python
llm = OctoAIEndpoint(
    endpoint_url="https://text.octoai.run/v1/chat/completions"
    ,
    model_kwargs={
        "model": "mixtral-8x7b-instruct-fp16",
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

And that's all folks! You now have a great scaffold to be building a fun turn by turn adventure game powered by the latest and greatest open source SMoE model out there!

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

Run `adventure.py` script to chat with the LLM hosted endpoint.
```bash
python3 adventure.py
```

### Example usage

```Prompt: start
Prompt: start

Response(3.8 sec):  Welcome to "Mars Mission: A Choose Your Own Adventure"! You're about to embark on a thrilling journey to plan a mission to land on Mars. To begin, please select one of the three character classes:

A) The Pilot - specializing in navigation, landing, and spacecraft control
B) The Scientist - providing expertise in Martian geology, atmospheric conditions, and potential lifeforms
C) The Engineer - excelling in designing and building Martian habitats, life support systems, and solving technical issues

Please enter A, B, or C to choose your character class.
```

## License

This project is licensed under the MIT License.

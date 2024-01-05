# Turn by Turn adventure

A turn by turn adventure game using Langchain and OctoAI LLM (here we're using Mixtral).

We're using Langchain memory to provide LLM with historical information so it can make forward progress in the adventure.

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

- Run `adventure.py` script to chat with the LLM hosted endpoint.
```bash
python3 adventure.py
```

- Example usage:

```Prompt: start
Prompt: start

Response(3.8 sec):  Welcome to "Mars Mission: A Choose Your Own Adventure"! You're about to embark on a thrilling journey to plan a mission to land on Mars. To begin, please select one of the three character classes:

A) The Pilot - specializing in navigation, landing, and spacecraft control
B) The Scientist - providing expertise in Martian geology, atmospheric conditions, and potential lifeforms
C) The Engineer - excelling in designing and building Martian habitats, life support systems, and solving technical issues

Please enter A, B, or C to choose your character class.
```

## Acknowlegements

This example was inspired by the choose your own adventure game by techwithtim: https://github.com/techwithtim/AI-Choose-Your-Own-Adventure-Game
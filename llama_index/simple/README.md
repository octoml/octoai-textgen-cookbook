# Using OctoAI with LlamaIndex
LlamaIndex' main goal is to manage the interactions between your language models and your private data, and therefore makes it a critical part of building interesting and highly capable applications.

## What you will build
We will publish a more comprehensive example. For the time being you can find quick starts on the files enclosed in this folder.


## What you will use



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

### Running the examples

Run the `embeddings.py` script to test the embeddings integration.
```bash
python3 embeddings.py
```

Run the `llm.py` script to test the LLM integration.
```bash
python3 llm.py
```

## License

This project is licensed under the MIT License.

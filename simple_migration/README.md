# Change 3 lines of code to migrate to OctoAI

OctoAI LLMs are available to use through an OpenAI compatible API. Even more, if you have been building or prototyping using OpenAI's Python SDK you can keep your code as it is and still use OctoAI's LLM models.

In this example we will show you how to change just three lines of code to make your Python application use OctoAI's Open Source models through OpenAI's Python SDK.


## What you will build
Migrate OpenAI's Python SDK example script to use OctoAI's LLM endpoints.

These are the three modifications necessary to achieve our goal:
1. Redefine `OPENAI_API_KEY` your API key environment variable to use your OctoAI key.
2. Redefine `OPENAI_BASE_URL` to point to `https://text.octoai.run/v1`
3. Change the model name to an Open Source model, for example: `llama-2-13b-chat-fp16`


## What you will use
We will only use Python and the OpenAI's Python SDK.

## Instructions

- Set up python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install the pip requirements in your local python virtual environment

```bash
python3 -m pip install openai
```

### Environment setup

To run this example app, there are two simple steps to take:

- Get an OctoAI API token by following [these instructions](https://octo.ai/docs/getting-started/how-to-create-octoai-api-token/).
- Expose the token in a new `OCTOAI_TOKEN` environment variable:

```bash
export OCTOAI_TOKEN=<your-token>
```
- Now source the provided `environment.sh` file:
```bash
source environment.sh
```

If you prefer, you can also directly paste your token in the file.

You will notice that we have done some of the changes for you:
* We have already added the `OPENAI_API_BASE` URL for you.
* We have already changed line 5 from the example to select Llama-2-13B as the model to use.

### Running the application

Run `response.py` script to chat with the LLM hosted endpoint.
```bash
python3 response.py
```

### Example output


## License

This project is licensed under the MIT License.

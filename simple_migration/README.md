# Change 3 lines of code to migrate to OctoAI

OctoAI LLMs are available to use through our OpenAI compatible API. Additionally, if you have been building or prototyping using OpenAI's Python SDK you can keep your code as-is and use OctoAI's LLM models.

In this example, we will show you how to change just three lines of code to make your Python application use OctoAI's Open Source models through OpenAI's Python SDK.


## What you will build
Migrate OpenAI's Python SDK example script to use OctoAI's LLM endpoints.

These are the three modifications necessary to achieve our goal:
1. Redefine `OPENAI_API_KEY` your API key environment variable to use your OctoAI key.
2. Redefine `OPENAI_BASE_URL` to point to `https://text.octoai.run/v1`
3. Change the model name to an Open Source model, for example: `llama-2-13b-chat-fp16`


## Requirements
We will be using Python and OpenAI's Python SDK.

## Instructions

- Set up a Python virtual environment. Read _Creating Virtual Environments_ [here](https://docs.python.org/3/library/venv.html).

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
- Source the provided `environment.sh` file:
```bash
source environment.sh
```

If you prefer, you can also directly paste your token in the file.

We have completed some of these tasks for you:
* We have already added the `OPENAI_API_BASE` URL for you.
* We have already changed line 5 from the example to select the `Llama-2-13B` model.

### Running the application

Run the `response.py` script to chat with the hosted LLM endpoint.
```bash
python3 response.py
```

### Example output
```bash
python response.py 
ChatCompletionMessage(content="  Hello! How can I assist you today? Do you have any questions or tasks you'd like help with? Please let me know and I'll do my best to assist you.", role='assistant', function_call=None, tool_calls=None)
```


## License

This project is licensed under the MIT License.

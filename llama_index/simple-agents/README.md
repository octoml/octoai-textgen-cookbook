# Simple LlamaIndex Agents in OctoAI

This project demonstrates how to build a LlamaIndex agent using OctoAI LLMs.

## Dependencies
This is a poetry based project. If you have not done so yet, please install [poetry](https://python-poetry.org/docs/#installation).

In order to set up your environment run:
```bash
export OCTOAI_API_KEY=<your api key>
poetry install --no-root
poetry shell
```

## Built-in tools
The release of Llama 3.1 by Meta introduced a new concept: [Built-in Tools](https://octo.ai/docs/text-gen-solution/function-calling/built-in):
* Brave Search: `brave_search`
* Wolfram Alpha: `wolfram_alpha`
* Code Interpreter: `code_interpreter`

The script `built-in-tools.py` demonstrates how to trigger the use of built-in functions through LlamaIndex agents.

You can run the script via:
```bash
python3 built-in-tools.py
```

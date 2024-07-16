# LangChain examples in OctoAI
This folder contains scripts managed by a poetry project.

## Dependencies
Install the dependencies via:
```bash
poetry install --no-root
```

## Running the examples
First define an environment variable with your token:
```bash
export OCTOAI_API_TOKEN="your-token"
```

Then get an active shell with the poetry environment:
```bash
poetry shell
```

Now you are ready to run the examples:
```bash
python3 embeddings.py
```

## What if I don't have poetry?
Just copy the requirements from `pyproject.toml` then use `pip install` as usual.

# ReAct Agent with OctoAI and LlamaIndex

## Installing requirements
This example is based on a Poetry project. See [this](https://python-poetry.org/docs/#installation) for installation instructions. This is a nice to have but not a hard requirement. See the following section for guidance on how to install dependencies without Poetry.

This example generates pdf files via [Pandoc](https://pandoc.org/installing.html?ref=gettingstarted.ai). Please install this dependency first.

Pandoc requires `pdflatex` to be available. An alternative for MacOS can be found via:
```bash
brew install --cask mactex-no-gui
```

### Python packages
Install with Poetry via:
```bash
poetry install --no-root
```

One can also use pip, just take a look at the dependencies in `pyproject.toml`

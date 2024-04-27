# Using LLMs for e-commerce applications
This is a simple example of things that can be done given a dataset of products, thinking on e-commerce applications.

This script is based on the [Amazon Reviews 2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) dataset.

This dataset is comprised of two parts:
* Product Metadata
* Product Reviews

In this project we use an LLM to undertake two task within a single API call. This is possible due to:
* OctoAI's guaranteed structured output, or JSON mode.
* Mixtral long context window of 32K tokens.

With a single API call we are:
* Generating titles and short description in all languages supported by Mixtral
* Generating short list of pro's and con's, based on users reviews.

# Requirements
This is a poetry based project, you will require python and [poetry](https://python-poetry.org/docs/).

After that, all other requirements can be installed via:
```bash
poetry install
```

# Running the example
Use a poetry shell to automatically use the virtual environment.

We also use `jq` to have a nice render of the output.
```bash
poetry shell
python main.py | jq
```

## Example output
```bash
$ python main.py | jq
{
  "english": {
    "description": "GQ Print Magazine: Culture-defining covers and elevated style",
    "title": "GQ Print Magazine"
  },
  "french": {
    "description": "Magazine imprimé GQ : Des couvertures définissant la culture et un style élevé",
    "title": "Magazine imprimé GQ"
  },
  "italian": {
    "description": "Rivista GQ a stampa: Copertine di cultura e stile elevato",
    "title": "Rivista GQ a stampa"
  },
  "german": {
    "description": "GQ Print-Magazin: Kulturprägende Cover und stilvolles Design",
    "title": "GQ Print-Magazin"
  },
  "spanish": {
    "description": "Revista GQ de impresión: Portadas definiendo la cultura y estilo elegante",
    "title": "Revista GQ de impresión"
  },
  "pros": [
    "Culture-defining covers",
    "Elevated style",
    "Respected reporting and writing"
  ],
  "cons": [
    "All advertisements"
  ]
}
```

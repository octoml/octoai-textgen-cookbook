# README

## Project Overview

This is a Python command line interface (CLI) application that takes as inputs a list of ingredients from the user and responds with a recipe for a dish that can be prepared from the provided list of ingredients. It demonstrates the ease with which large language models (LLM) powered logic and reasoning can be integrated into applications to deliver engaging experiences to end users. The application uses the OctoAI Python SDK and the Llama 2 13B Chat model on the OctoAI Text Gen Solution.

## Features
	•	OctoAI Python sdk (octoai-sdk) 
	•	Text generation using Llama 2, using the OpenAI chat completions API
	•	Use of the OctoAI LLM endpoints for language understanding and processing.

## Prerequisites

Before running this application, you need to have Python installed on your system along with the application dependencies. You can install these packages using pip:

`pip install -r requirements.txt`

Additionally, you need to set up a `.env` file in the root of the project with the necessary environment variables.

-   To get an OctoAI API Token: please follow the steps here https://docs.octoai.cloud/docs/how-to-create-an-octoai-access-token

## Environment Variables

Make sure you have the `.env` file in the project's `app` directory, following this template:

```
OCTOAI_TOKEN=YOUR-TOKEN
```

Replace the placeholder values with your actual API key.

## Running the Application

To run the application via CLI, execute the main script:

`python octofridge.py`

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License.

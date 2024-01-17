# How to build a food recipe generator with OctoAI SDK and Llama2 LLM

This is a Python command line interface (CLI) application that takes a list of ingredients from the user as inputs and responds with a recipe for a dish that can be prepared from the provided list of ingredients. 

It demonstrates the ease with which large language models (LLM) powered logic and reasoning can be integrated into applications to deliver engaging experiences to end users. 

The application uses the OctoAI Python SDK and the Llama 2 13B Chat model on the OctoAI Text Gen Solution.

## Features

This example doesn't rely on Langchain and uses the OctoAI SDK directly, which is OpenAI API compatible! Here are the features that you'll be using to build your recipe generator:

* OctoAI Python sdk (octoai-sdk)
* Text generation with Llama 2, using the OpenAI chat completions API
* Use of the OctoAI LLM endpoints for language understanding and processing.

## Instructions

Before running this application, you need to have Python installed on your system along with the application dependencies. You can install these packages using pip and python virtual environment.

Set up python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the pip requirements in your local python virtual environment

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

To run the application in your terminal, execute the main script:

- Run `recipe_generator.py` script to chat with the LLM hosted endpoint.
```bash
python3 recipe_generator.py
```

### Example usage
```text
Welcome to OctoFridge!
Enter the ingredients in your fridge in a comma separated list and hit <enter> : eggs, butter, sugar, lemon, flour, salt

Sure! Here is a recipe for a delicious Lemon Egg Butter Cake that uses all of the ingredients you provided:

Ingredients:

* 4 eggs
* 1/2 cup (1 stick) unsalted butter, softened
* 1 1/2 cups granulated sugar
* 1/2 cup freshly squeezed lemon juice
* 2 1/4 cups all-purpose flour
* 1 teaspoon salt

Instructions:

1. Preheat your oven to 350°F (180°C). Grease a 9-inch (23cm) round cake pan and set it aside.
2. In a large mixing bowl, cream together the butter and sugar until light and fluffy. Beat in the eggs one at a time, making sure each egg is fully incorporated before adding the next.
3. Add the lemon juice and mix until well combined.
4. In a separate bowl, whisk together the flour and salt. Gradually add the dry ingredients to the wet ingredients, mixing until just combined.
5. Pour the batter into the prepared cake pan and smooth the top.
6. Bake for 35-40 minutes, or until a toothpick inserted into the center of the cake comes out clean.
7. Remove the cake from the oven and let it cool in the pan for 5 minutes, then transfer it to a wire rack to cool completely.
8. Once the cake is cool, dust it with powdered sugar and serve slices with a dollop of lemon whipped cream, if desired.

Enjoy your delicious Lemon Egg Butter Cake!
```

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License.

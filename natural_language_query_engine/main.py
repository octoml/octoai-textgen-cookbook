import json
import os

import gradio as gr
from dotenv import find_dotenv
from dotenv import load_dotenv

from services.db_client import CouchbaseClient
from services.nlq_engine import CouchbaseNLQEngine

# Load environment variables from a .env file if present
load_dotenv(find_dotenv())

# Initialize the Couchbase client and natural language query engine
client = CouchbaseClient()
engine = CouchbaseNLQEngine(client)


def load_collection_schemas():
    """
    Loads the collection schemas from a JSON file if it exists; otherwise, generates the schemas using the engine
    and saves them to the file.

    Returns:
        dict: A dictionary containing the schemas of the collections.
    """
    schemas_path = os.path.join("resources", "collection_schemas.json")
    if os.path.exists(schemas_path):
        # Load existing schemas from file
        with open(schemas_path, "r") as f:
            return json.load(f)
    else:
        # Generate schemas if the file does not exist and save them
        collection_schemas = engine.generate_db_schema()
        with open(schemas_path, "w") as f:
            json.dump(collection_schemas, f)

        return collection_schemas


# Load or generate the collection schemas
schemas = load_collection_schemas()


def handle_query(query):
    """
    Handles the input natural language query, executing it against the Couchbase database.

    Args:
        query (str): The natural language query input by the user.

    Returns:
        list[dict]: The raw results from the Couchbase database in JSON format.
    """
    _, results = engine.run_query(schemas, query)
    return results


# Define the Gradio interface for querying the Couchbase database
interface = gr.Interface(
    fn=handle_query,
    inputs="text",
    outputs="json",
    title="Couchbase Natural Language Query",
    description="Enter a natural language query and get raw results from Couchbase in JSON format.",
)

# Launch the Gradio interface
interface.launch()

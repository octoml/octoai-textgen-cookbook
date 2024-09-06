import json
import os
import os.path

from dotenv import find_dotenv
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOctoAI
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate

from config.constants import COLLECTIONS
from services.db_client import CouchbaseClient

# Load environment variables from a .env file if present
load_dotenv(find_dotenv())


class CouchbaseNLQEngine:
    """
    A class to interact with a Couchbase database using natural language queries (NLQ)
    powered by language models from OctoAI.

    Attributes:
        client (CouchbaseClient): An instance of the CouchbaseClient class for database operations.
        llm (OctoAIEndpoint): An instance of OctoAIEndpoint for executing large language model prompts.
        chat_llm (ChatOctoAI): An instance of ChatOctoAI for chat-based interactions with the language model.
        proofread_query_prompt (str): The template for proofreading queries.
        schema_generation_prompt (str): The template for generating database schema.
        query_generation_prompt (str): The template for generating SQL++ queries.
    """

    def __init__(
        self,
        client: CouchbaseClient,
        model: str = "meta-llama-3.1-70b-instruct",
        max_tokens: int = 2048,
        presence_penalty: int = 0,
        temperature: float = 0.0,
        top_p: float = 1,
        prompts_directory: str = os.path.join("resources", "prompts"),
    ):
        """
        Initializes the CouchbaseNLQEngine with the given configuration and loads prompts from files.

        Args:
            client (CouchbaseClient): A CouchbaseClient instance for interacting with the database.
            model (str): The model identifier for the language model. Defaults to 'meta-llama-3.1-70b-instruct'.
            max_tokens (int): The maximum number of tokens to generate. Defaults to 2048.
            presence_penalty (int): The presence penalty parameter for the language model. Defaults to 0.
            temperature (float): Sampling temperature for the language model. Defaults to 0.0.
            top_p (float): Nucleus sampling parameter. Defaults to 1.
            prompts_directory (str): Directory path to the prompt templates. Defaults to 'resources/prompts'.
        """
        self.client = client
        self.llm = OctoAIEndpoint(
            model=model,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            temperature=temperature,
            top_p=top_p,
        )
        self.chat_llm = ChatOctoAI(
            model=model, max_tokens=max_tokens, temperature=temperature
        )

        # Load prompt templates for query proofing, schema generation, and query generation
        with open(os.path.join(prompts_directory, "proofread_query.txt"), "r") as f:
            self.proofread_query_prompt = f.read()

        with open(os.path.join(prompts_directory, "schema_generation.txt"), "r") as f:
            self.schema_generation_prompt = f.read()

        with open(os.path.join(prompts_directory, "query_generation.txt"), "r") as f:
            self.query_generation_prompt = f.read()

    def generate_db_schema(self) -> dict:
        """
        Generates the schema for each collection in the Couchbase database using the language model.

        Returns:
            dict: A dictionary containing generated schemas for each collection.

        Raises:
            Exception: If there is an error in generating or parsing the schema.
        """
        prompt = PromptTemplate.from_template(self.schema_generation_prompt)
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)

        collection_schemas = {}
        for collection in COLLECTIONS:
            sample = self.client.get_sample(collection=collection, limit=20)

            print(f"Generating schema for {collection}...")
            response = llm_chain.invoke(
                {
                    "collection": collection,
                    "sample": json.dumps(sample),
                },
            )["text"]

            # Clean the response and parse it as JSON
            schema = json.loads(
                response.strip().replace("```json", "").replace("```", "")
            )
            collection_schemas[collection] = schema

        return collection_schemas

    def proofread_query(self, query: str) -> str:
        """
        Proofreads and corrects a natural language query using the language model.

        Args:
            query (str): The query string to be proofread.

        Returns:
            str: The corrected query string.

        Raises:
            Exception: If there is an error in the proofreading process.
        """
        prompt = PromptTemplate.from_template(self.proofread_query_prompt)
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)

        response = llm_chain.invoke(
            {
                "query": query,
            },
        )["text"]

        # Parse the corrected query from the response
        corrected_query = json.loads(
            response.strip().replace("```json", "").replace("```", "")
        )

        return corrected_query["query"]

    def run_query(
        self, collection_schemas: dict, query: str, max_retries=3
    ) -> list[dict]:
        """
        Executes a query against the Couchbase database, using the language model for query generation.

        Args:
            collection_schemas (dict): A dictionary containing schema information for each collection.
            query (str): The query to be executed.
            max_retries (int): Maximum number of retries for query generation in case of errors. Defaults to 3.

        Returns:
            str: SQL++ query.
            list[dict]: A list of query results.

        Raises:
            Exception: If the query fails to generate after the specified number of retries.
        """
        # Proofread the input query using the language model
        print("Original query:", query)
        query = self.proofread_query(query)
        print("Proofread query:", query)

        # Prepare system and human messages for the chat model
        messages = [
            SystemMessage(
                content="You are an agent designed to interact with a Couchbase database, using SQL++."
            ),
            HumanMessage(
                content=self.query_generation_prompt.replace("{query}", query)
                .replace("{schemas}", json.dumps(collection_schemas))
                .replace("{collections}", ",".join(COLLECTIONS))
            ),
        ]

        retries_left = max_retries
        while retries_left > 0:
            try:
                print("Generating query...")
                # Generate the SQL++ query using the chat model
                generated_query = self.chat_llm.invoke(messages).content
                messages.append(AIMessage(content=generated_query))

                # Clean the generated query string
                generated_query = generated_query.replace("```sql", "").replace(
                    "```", ""
                )

                print(generated_query)

                print("Query generated successfully.")
                # Execute the generated query against the Couchbase database
                return generated_query, self.client.run_raw_query(generated_query)
            except Exception as e:
                # Handle errors by appending a retry message and decrementing the retry count
                messages.append(
                    HumanMessage(
                        content=f"There was an error: {e}. Try again. Only return the fixed SQL++ query. Don't say anything else"
                    )
                )
                retries_left -= 1

        # Raise an exception if all retries are exhausted
        if retries_left == 0:
            raise Exception(f"Failed to generate query after {max_retries} retries.")

import os
import traceback
from datetime import timedelta

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from dotenv import find_dotenv
from dotenv import load_dotenv

from config.constants import CLUSTER_BUCKET
from config.constants import SCOPE

# Load environment variables from a .env file if present
load_dotenv(find_dotenv())


class CouchbaseClient:
    """
    A client class to interact with Couchbase database using Python SDK.

    Attributes:
        url (str): The URL of the Couchbase server.
        username (str): The username for authenticating with Couchbase.
        password (str): The password for authenticating with Couchbase.
        cluster (Cluster): The Couchbase cluster instance for executing queries.
    """

    def __init__(self):
        """
        Initializes the CouchbaseClient class by setting up connection credentials
        and connecting to the Couchbase cluster.
        """
        # Retrieve Couchbase connection details from environment variables
        self.url = os.environ["COUCHBASE_URL"]
        self.username = os.environ["COUCHBASE_USERNAME"]
        self.password = os.environ["COUCHBASE_PASSWORD"]

        # Set up authentication and cluster options
        auth = PasswordAuthenticator(self.username, self.password)
        options = ClusterOptions(auth)

        # Apply WAN development profile for connection optimization
        options.apply_profile("wan_development")

        # Connect to the Couchbase cluster and wait until ready
        self.cluster = Cluster(self.url, options)
        self.cluster.wait_until_ready(timedelta(seconds=5))

        print("Connected to Couchbase")

    def get_sample(self, collection: str, limit: int = 10) -> list[dict]:
        """
        Retrieves a sample of documents from the specified collection.

        Args:
            collection (str): The name of the collection from which to retrieve documents.
            limit (int): The maximum number of documents to retrieve. Defaults to 10.

        Returns:
            list[dict]: A list of documents retrieved from the collection.

        Raises:
            Exception: If there is an error while executing the query.
        """
        try:
            # Execute a raw N1QL query to fetch documents from the specified collection
            return self.run_raw_query(f"SELECT * FROM {collection} LIMIT {limit}")
        except Exception as e:
            # Handle exceptions by printing error message and traceback
            print("Failed to get sample", e)
            print(traceback.format_exc())

    def run_raw_query(self, query: str) -> list[dict]:
        """
        Executes a raw N1QL query on the Couchbase cluster.

        Args:
            query (str): The N1QL query string to execute.

        Returns:
            list[dict]: A list of query results as dictionaries.

        Raises:
            Exception: If there is an error while executing the query.
        """
        try:
            # Access the specified bucket and scope within the Couchbase cluster
            cb = self.cluster.bucket(CLUSTER_BUCKET)
            inventory_scope = cb.scope(SCOPE)

            # Execute the query and convert results to a list
            row_iter = inventory_scope.query(query)
            return list(row_iter)
        except Exception as e:
            # Print traceback and re-raise the exception
            print(traceback.format_exc())
            raise e

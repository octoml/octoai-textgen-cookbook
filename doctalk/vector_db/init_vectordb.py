import json
import os
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Chunking configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 20

# Environment Variables
OCTOAI_TOKEN = os.environ.get("OCTOAI_TOKEN")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV")

if OCTOAI_TOKEN is None:
    raise ValueError("OCTOAI_TOKEN environment variable not set.")
if PINECONE_API_KEY is None:
    raise ValueError("PINECONE_API_KEY environment variable not set.")
if PINECONE_ENV is None:
    raise ValueError("PINECONE_ENV environment variable not set.")


# Utility Functions
def load_urls(file_path_list):
    url_list = []
    for file_path in file_path_list:
        with open(file_path, "r") as file:
            url_list += [item["url"] for item in json.load(file)]
    return url_list


if __name__ == "__main__":

    # Name our index on Pinecone
    pinecone_index_name = "doctalk"

    # Init pinecone
    pc = Pinecone(
        api_key=PINECONE_API_KEY,
        source_tag="octoai-doctalk"
    )

    # First initialize the vector store
    print("Creating the Pinecone index...")
    if pinecone_index_name in pc.list_indexes().names():
        print("Index {} already created".format(pinecone_index_name))
        exit()
    else:
        pc.create_index(
            name='doctalk',
            dimension=1024,
            metric='euclidean',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        # Wait for index to be initialized
        while not pc.describe_index(pinecone_index_name).status["ready"]:
            # TODO remove me
            print("sleeping")
            time.sleep(1)

    # Second, load all of the content we want to populate
    print("Loading the information from the websites")
    # Dictionary containing all of the URLs
    urls = load_urls(["data/pinecone_docs_urls.json", "data/octoai_docs_urls.json"])
    # Get the doc pages documentation
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    transformed_docs = BeautifulSoupTransformer().transform_documents(
        docs, tags_to_extract=["div"]
    )

    # Third, let's split the chunks
    print("Splitting the website information into chunks")
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    splits = splitter.split_documents(transformed_docs)

    # Initialize the vector store with the OctoAI embedding
    print("Initializing the Pinecone VectorStore")
    embeddings = OctoAIEmbeddings(
        endpoint_url="https://text.octoai.run/v1/embeddings",
        octoai_api_token=OCTOAI_TOKEN,
    )
    # OctoAI embedding
    vectorstore = PineconeVectorStore(
        index_name=pinecone_index_name,
        embedding=embeddings
    )

    # Upsert documents
    print("Upserting the vectors into the database")
    vectorstore.add_documents(splits)

    print("Done!")

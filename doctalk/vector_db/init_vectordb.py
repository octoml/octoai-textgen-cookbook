import os
import json
import uuid
import time
import pinecone
import pandas as pd
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration Constants
TRANSFORMERS_CACHE_DIR = "/tmp/transformers_cache"
PINECONE_DB_NAME = "pinecone_pinecone_docs"
BATCH_SIZE = 1  # Needs to be 1 for GTE model for now
CHUNK_SIZE = 1300
CHUNK_OVERLAP = 5
PHRASE_LENGTH = 30

# Environment Variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV", "PINECONE_ENV")
OCTOAI_TOKEN = os.environ.get("OCTOAI_TOKEN")

if OCTOAI_TOKEN is None:
    raise ValueError("OCTOAI_TOKEN environment variable not set.")

# Set cache directory for transformers
os.environ["HF_HOME"] = TRANSFORMERS_CACHE_DIR
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Utility Functions
def load_urls(file_path):
    with open(file_path, "r") as file:
        return [item["url"] for item in json.load(file)]


def extract(content):
    return {"page_content": str(BeautifulSoup(content, "html.parser").contents)}


def process_documents(urls):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    transformed_docs = BeautifulSoupTransformer().transform_documents(
        docs, tags_to_extract=["div"]
    )
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    splits = splitter.split_documents(transformed_docs)
    return [extract(split.page_content) for split in splits]


def find_common_phrases(contents, phrase_length=30):
    reference_content = contents[0]["page_content"]
    tokens = reference_content.split()
    return {
        " ".join(tokens[i : i + phrase_length])
        for i in range(len(tokens) - phrase_length + 1)
        if all(
            " ".join(tokens[i : i + phrase_length]) in content["page_content"]
            for content in contents
        )
    }


def remove_common_phrases_from_contents(contents, common_phrases):
    for content in contents:
        for phrase in common_phrases:
            content["page_content"] = content["page_content"].replace(phrase, "")
    return contents


def get_octo_embed_model():
    return OctoAIEmbeddings(
        endpoint_url="https://text.octoai.run/v1/embeddings",
        octoai_api_token=OCTOAI_TOKEN,
    )


def add_pinecone_embeddings(data, index_name):
    embed = get_octo_embed_model()
    batch_size = BATCH_SIZE
    for i in range(0, len(data), batch_size):
        i_end = min(len(data), i + batch_size)
        # get batch of data
        batch = data.iloc[i:i_end]
        # generate unique ids for each chunk
        ids = [f"{x['id']}" for i, x in batch.iterrows()]
        # get text to embed
        texts = [x["text"] for _, x in batch.iterrows()]
        # embed text
        embeds = embed.embed_documents(texts)
        # get metadata to store in Pinecone
        metadata = [{"text": x["text"][:4000]} for i, x in batch.iterrows()]
        # add to Pinecone
        index = pinecone.Index(index_name)
        index.upsert(vectors=zip(ids, embeds, metadata))

    return index


def get_pinecone_dataframe(extracted_contents):
    df = pd.DataFrame(columns=["id", "text"])
    # Loop through each item in extracted_contents and append it to the DataFrame
    for item in extracted_contents:
        # Generate a new GUID for each row
        guid = str(uuid.uuid4())

        # Extract the text using the key "page_content"
        text = str(item["page_content"])

        # Append the new row to the DataFrame
        df = df._append({"id": guid, "text": text}, ignore_index=True)

    return df


def init_pinecone_index(index_name="doctalk"):
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV,
    )

    if index_name in pinecone.list_indexes():
        print("Index {} already created".format(index_name))
        exit()
    else:
        # Create the new index with the cosine similarity function
        # Make sure to size the vectors according to the embedding model you're using
        # In this case we set to 1024 because we're using GTE-Large on OctoAI
        pinecone.create_index(
            name=index_name,
            metric="cosine",
            dimension=1024
        )

        # Wait for index to be initialized
        while not pinecone.describe_index(index_name).status["ready"]:
            time.sleep(1)

    return index_name


if __name__ == "__main__":

    # Name our index on Pinecone
    pinecone_index_name = "doctalk"

    # First initialize the vector store
    print("Initializing the Pinecone index...")
    _ = init_pinecone_index(index_name=pinecone_index_name)

    # Second, load all of the content we want to populate
    print("Loading the content we want to run RAG on, this could take a couple of minutes...")
    # Dictionary containing all of the URLs
    urls = load_urls("data/pinecone_docs_urls.json")
    # Extract content using AsyncChromiumLoader
    extracted_contents = process_documents(urls)

    # Third pre-process the data before storing in vector store
    print("Preprocessing the data before storing in the vector DB")
    common_phrases = find_common_phrases(extracted_contents)
    extracted_contents_modified = remove_common_phrases_from_contents(
        extracted_contents, common_phrases
    )
    data = get_pinecone_dataframe(extracted_contents_modified)

    # Finally add the pinecone embeddings
    print("Adding the vector embeddings into the database, this could take a couple of minutes...")
    add_pinecone_embeddings(data, pinecone_index_name)

    print("Done!")

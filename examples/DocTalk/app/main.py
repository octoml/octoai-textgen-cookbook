import os
import json
import uuid
import time
import pinecone
import pandas as pd
from bs4 import BeautifulSoup
from langchain.llms.octoai_endpoint import OctoAIEndpoint
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.embeddings import OctoAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Configuration Constants
TRANSFORMERS_CACHE_DIR = "/tmp/transformers_cache"
OCTOAI_JSON_FILE_PATH = "data/octoai_docs_urls.json"
PINECONE_JSON_FILE_PATH = "data/pinecone_docs_urls.json"
OCTOAI_DB_NAME = "pinecone_octoai_docs"
PINECONE_DB_NAME = "pinecone_pinecone_docs"
OCTOAI_EMBED_ENDPOINT_URL = "https://instructor-large-f1kzsig6xes9.octoai.run/predict"
BATCH_SIZE = 100
CHUNK_SIZE = 1300
CHUNK_OVERLAP = 5
PHRASE_LENGTH = 30
SHOW_RESP_TIME = False
# Environment Variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV", "PINECONE_ENV")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX", "rag")
OCTOAI_TOKEN = os.environ.get("OCTOAI_TOKEN")
OCTOAI_ENDPOINT = os.environ.get("ENDPOINT_URL")
OCTOAI_MODEL = os.environ.get("MODEL")

if OCTOAI_TOKEN is None:
    raise ValueError("OCTOAI_TOKEN environment variable not set.")

# Set cache directory for transformers
os.environ["TRANSFORMERS_CACHE"] = TRANSFORMERS_CACHE_DIR
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Utility Functions
def load_urls(file_path):
    with open(file_path, "r") as file:
        return [item["url"] for item in json.load(file)]


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


def extract(content):
    return {"page_content": str(BeautifulSoup(content, "html.parser").contents)}


def tokenize(text):
    return text.split()


def find_common_phrases(contents, phrase_length=30):
    reference_content = contents[0]["page_content"]
    tokens = tokenize(reference_content)
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


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def process_text_files(filepath="data/shakespeare.txt"):
    docs_transformed = read_file(filepath)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1300, chunk_overlap=5)
    splits = splitter.split_text(docs_transformed)
    return [extract(split) for split in splits]


def get_octo_embed_model():
    return OctoAIEmbeddings(
        endpoint_url=OCTOAI_EMBED_ENDPOINT_URL,
        octoai_api_token=OCTOAI_TOKEN,
    )


def get_embeddings(db_name=OCTOAI_DB_NAME):
    embed = get_octo_embed_model()
    return embed.embed_documents(db_name)


def add_pinecone_embeddings(data, index_name):
    embed = get_octo_embed_model()
    batch_size = 100
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


def get_dataframe_for_pinecone(embeddings):
    df = pd.DataFrame(embeddings)
    df.columns = ["id", "text"]
    return df


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


def add_documents_to_vectorstore(extracted_contents, vectorstore):
    for item in extracted_contents:
        doc = Document.parse_obj(item)
        doc.page_content = str(item["page_content"])
        vectorstore.add_documents([doc])


def init_pinecone_index(index_name=PINECONE_INDEX_NAME):
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV,
    )

    if not index_name in pinecone.list_indexes():
        # pinecone.delete_index(index_name)
        # we create a new index
        pinecone.create_index(
            name=index_name,
            metric="dotproduct",
            dimension=768,  # instructor-large dimension
        )

        # wait for index to be initialized
        while not pinecone.describe_index(index_name).status["ready"]:
            time.sleep(1)

    #index = pinecone.Index(index_name)

    # print(index.describe_index_stats())

    return index_name


def get_pinecone_vector_store(index_name=PINECONE_INDEX_NAME):
    text_field = "text"  # the metadata field that contains our text
    embed_model = get_octo_embed_model()
    index_name = init_pinecone_index(index_name=index_name)
    index = pinecone.Index(index_name)
    # initialize the vector store object
    vectorstore = Pinecone(index, embed_model.embed_query, text_field)

    return vectorstore


def get_language_models():
    return OctoAIEndpoint(
        octoai_api_token=OCTOAI_TOKEN,
        endpoint_url=OCTOAI_ENDPOINT,
        model_kwargs={
            "messages": [
                {
                    "role": "system",
                    "content": "Write a response that appropriately completes the request. Be clear and concise. Format your response as bullet points whenever possible.",
                }
            ],
            "model": OCTOAI_MODEL,
            "max_tokens": 200,
        },
    )


def execute_and_print(llm, retriever, question, model_name):
    start_time = time.time()
    openai_usage_str = ""

    qa = ConversationalRetrievalChain.from_llm(llm, retriever, max_tokens_limit=2000)
    response = qa({"question": question, "chat_history": []})

    end_time = time.time()
    result = f"\n{model_name}\n"
    result += response["answer"]

    if SHOW_RESP_TIME == "True":
        result += f"\n\nResponse ({round(end_time - start_time, 1)} sec)"

    return result


def predict(data_source="octoai_docs", prompt="how to avoid cold starts?"):
    schema = {
        "properties": {"page_content": {"type": "string"}},
        "required": ["page_content"],
    }

    if "pinecone" in data_source.lower():
        db_name = PINECONE_DB_NAME
    elif "octo" in data_source.lower():
        db_name = OCTOAI_DB_NAME

    llm_llama2 = get_language_models()

    index_name = PINECONE_INDEX_NAME
    init_pinecone_index(index_name=index_name)
    index = pinecone.Index(index_name)

    if (
        index.describe_index_stats()["total_vector_count"] < 10
    ):  # if index was not populated
        
        print("Populating index for the first time...This might take several minutes")
        
        url_file = (
            OCTOAI_JSON_FILE_PATH
            if db_name == OCTOAI_DB_NAME
            else PINECONE_JSON_FILE_PATH
        )
        urls = load_urls(url_file)

        extracted_contents = process_documents(urls)
        common_phrases = find_common_phrases(extracted_contents)
        extracted_contents_modified = remove_common_phrases_from_contents(
            extracted_contents, common_phrases
        )
        data = get_pinecone_dataframe(extracted_contents_modified)
        add_pinecone_embeddings(data, index_name)

    vectorstore = get_pinecone_vector_store(index_name)

    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 2}
    )

    result = execute_and_print(llm_llama2, retriever, prompt, "#LLAMA-2#")

    return result.strip("\n")  # Join and return combined results


# Main Handler Function for when the code is used as an AWS lambda function
def handler(event, context):
    body = json.loads(event["body"])
    data_source = body.get("data_source", None)
    prompt = body.get("prompt", None)
    answer = predict(data_source, prompt)
    return {"statusCode": 200, "body": json.dumps({"message_llm1": answer.strip("\n")})}


# CLI interaction
if __name__ == "__main__":
    print("Enter the data source (e.g., 'octoai_docs', 'pinecone_docs'):")
    data_source = input().strip()

    print("Enter your prompt:")
    prompt = input().strip()

    # Example event and context
    event = {"body": json.dumps({"data_source": data_source, "prompt": prompt})}

    context = {}
    response = handler(event, context)
    print("Response:", response)

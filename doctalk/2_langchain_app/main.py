import os
import json
import time
import pinecone
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.vectorstores import Pinecone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Configuration Constants
TRANSFORMERS_CACHE_DIR = "/tmp/transformers_cache"
# Show the response time
SHOW_RESP_TIME = False
# Environment Variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV", "PINECONE_ENV")
OCTOAI_TOKEN = os.environ.get("OCTOAI_TOKEN")
OCTOAI_ENDPOINT_URL = os.environ.get("OCTOAI_ENDPOINT_URL")
OCTOAI_MODEL = os.environ.get("OCTOAI_MODEL")

if OCTOAI_TOKEN is None:
    raise ValueError("OCTOAI_TOKEN environment variable not set.")

# Set cache directory for transformers
os.environ["HF_HOME"] = TRANSFORMERS_CACHE_DIR
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Utility Functions
def get_octo_embed_model():
    return OctoAIEmbeddings(
        endpoint_url="https://text.octoai.run/v1/embeddings",
        octoai_api_token=OCTOAI_TOKEN,
    )


def get_pinecone_vector_store(index_name):
    text_field = "text"  # the metadata field that contains our text
    embed_model = get_octo_embed_model()
    index = pinecone.Index(index_name)
    # initialize the vector store object
    vectorstore = Pinecone(index, embed_model, text_field)

    return vectorstore


def get_language_models():
    return OctoAIEndpoint(
        octoai_api_token=OCTOAI_TOKEN,
        endpoint_url=OCTOAI_ENDPOINT_URL,
        model_kwargs={
            "messages": [
                {
                    "role": "system",
                    "content": "Write a response that appropriately completes the request. Be clear and concise. Format your response as bullet points whenever possible.",
                }
            ],
            "model": OCTOAI_MODEL,
            "max_tokens": 1024,
        },
    )


def execute_and_print(llm, retriever, question, model_name):
    start_time = time.time()

    try:
        qa = ConversationalRetrievalChain.from_llm(
            llm, retriever, max_tokens_limit=2000
        )
        response = qa.invoke({"question": question, "chat_history": []})
    except Exception as e:
        print(e)
        exit(1)

    end_time = time.time()
    result = f"\n{model_name}\n"
    result += response["answer"]

    if SHOW_RESP_TIME == "True":
        result += f"\n\nResponse ({round(end_time - start_time, 1)} sec)"

    return result


def predict(prompt="how to avoid cold starts?"):

    try:
        llm = get_language_models()
    except Exception as e:
        print("Error initializing language models")
        print(e)
        exit(1)

    # Get Pinecone vector store, the index_name should match step 1
    index_name = "doctalk"
    vectorstore = get_pinecone_vector_store(index_name)

    # Perform similarity search on top-5 answers
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    # Run the LLM RAG chain to answer the question
    result = execute_and_print(llm, retriever, prompt, "#OctoAI LLM#")

    return result.strip("\n")  # Join and return combined results


# Main Handler Function for when the code is used as an AWS lambda function
def handler(event, context):
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV,
    )
    body = json.loads(event["body"])
    prompt = body.get("prompt", None)
    answer = predict(prompt)
    return {"statusCode": 200, "body": json.dumps({"message_llm1": answer.strip("\n")})}


# CLI interaction
if __name__ == "__main__":
    print("Enter your prompt:")
    prompt = input().strip()

    # Example event and context
    event = {"body": json.dumps({"prompt": prompt})}

    # Use handler to provide a response
    response = handler(event, {})
    print("Response:", (json.loads(response["body"])["message_llm1"]))

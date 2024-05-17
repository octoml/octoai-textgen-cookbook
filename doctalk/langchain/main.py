import os
import json
import time
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain_community.embeddings import OctoAIEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Show the response time
SHOW_RESP_TIME = True
# Environment Variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV", "PINECONE_ENV")
OCTOAI_TOKEN = os.environ.get("OCTOAI_TOKEN")
OCTOAI_ENDPOINT_URL = os.environ.get("OCTOAI_ENDPOINT_URL", "https://text.octoai.run/v1")
OCTOAI_MODEL = os.environ.get("OCTOAI_MODEL", "meta-llama-3-70b-instruct")

if OCTOAI_TOKEN is None:
    raise ValueError("OCTOAI_TOKEN environment variable not set.")
if PINECONE_API_KEY is None:
    raise ValueError("PINECONE_API_KEY environment variable not set.")
if PINECONE_ENV is None:
    raise ValueError("PINECONE_ENV environment variable not set.")


def predict(pc, user_question="how to avoid cold starts?"):

    # LLM init
    llm = OctoAIEndpoint(
        model="meta-llama-3-70b-instruct",
        max_tokens=2048,
        temperature=0.01
    )

    # Embedding init
    embeddings = OctoAIEmbeddings(
        endpoint_url="https://text.octoai.run/v1/embeddings",
        octoai_api_token=OCTOAI_TOKEN,
    )

    # Get Pinecone vector store, the index_name should match step 1
    index_name = "doctalk"
    text_field = "text"  # the metadata field that contains our text
    index = pc.Index(index_name)
    vectorstore = PineconeVectorStore(
        index, embeddings, text_field
    )

    # Retrieval Q&A chain with sources
    # We do similarity search and return the top 5 results
    qa = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
    )

    # Time the RAG
    start_time = time.time()
    response = qa(user_question)
    end_time = time.time()

    # Prepare the return string
    result = f"\n#OctoAI LLM#\n"
    result += response["answer"]
    result += "\n\nSources: {}".format(response["sources"])
    if SHOW_RESP_TIME == True:
        result += "\n\nResponse: {:.2f}s".format(end_time - start_time)

    return result.strip("\n")


# Main Handler Function for when the code is used as an AWS lambda function
def handler(event, context):
    try:
        # Init pinecone
        pc = Pinecone(
            api_key=PINECONE_API_KEY,
            source_tag="octoai-doctalk"
        )
        # Run RAG and format the response accordingly
        body = json.loads(event["body"])
        prompt = body.get("prompt", None)
        answer = predict(pc, prompt)
        return {"statusCode": 200, "body": json.dumps({"message_llm1": answer.strip("\n")})}
    except:
        return {"statusCode": 500, "body": "Something went wrong running RAG on the AWS Lambda"}


# CLI interaction
if __name__ == "__main__":
    print("Enter your prompt:")
    prompt = input().strip()

    # Example event and context
    event = {"body": json.dumps({"prompt": prompt})}

    # Use handler to provide a response
    response = handler(event, {})
    print("Response:", (json.loads(response["body"])["message_llm1"]))

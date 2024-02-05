import os
from dotenv import load_dotenv

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OctoAIEmbeddings

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory
os.chdir(current_dir)

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    loader = TextLoader("state_of_the_union.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    # embeddings = OctoAIEmbeddings(
    #     endpoint_url="https://text.octoai.run/v1/embeddings"
    # )
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    # Querying
    query = "What did the president say about Ketanji Brown Jackson"
    docs = db.similarity_search(query)
    print(docs[0].page_content)

from llama_index.embeddings.octoai import OctoAIEmbedding
from os import environ

OCTOAI_API_KEY = environ.get("OCTOAI_TOKEN")
embed_model = OctoAIEmbedding(api_key=OCTOAI_API_KEY)

# Single embedding request
embeddings = embed_model.get_text_embedding("Once upon a time in Seattle.")
assert len(embeddings) == 1024
print(embeddings[:10])


# Batch embedding request
texts = ["Once upon a time in Seattle.", "This is a test.", "Hello, world!"]
embeddings = embed_model.get_text_embedding_batch(texts)
assert len(embeddings) == 3
print(embeddings[0][:10])

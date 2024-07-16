from langchain_community.embeddings.octoai_embeddings import OctoAIEmbeddings

embeddings = OctoAIEmbeddings()
text = "This is a test query."
query_result = embeddings.embed_query(text)
print(query_result)

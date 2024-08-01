import os

from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.readers.file import PDFReader

data = PDFReader().load_data(file="guidelines.pdf")


index = VectorStoreIndex.from_documents(data, show_progress=False)


query_engine = index.as_query_engine()

guidelines_engine = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="guidelines_engine",
        description="This tool can retrieve content from the guidelines",
    ),
)

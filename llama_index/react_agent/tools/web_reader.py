# web_reader.py

from llama_index.core import SummaryIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.readers.web import SimpleWebPageReader


url = "https://www.gettingstarted.ai/crewai-beginner-tutorial"

documents = SimpleWebPageReader(html_to_text=True).load_data([url])
index = SummaryIndex.from_documents(documents)

query_engine = index.as_query_engine()

web_reader_engine = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="web_reader_engine",
        description="This tool can retrieve content from a web page",
    ),
)

# 2. Recursive Character Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter

raw_text = """
LangChain is a framework for developing applications powered by language models.
It provides tools for prompt management, chains, agents, and retrieval.
"""

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)

docs = text_splitter.create_documents([raw_text])

for i, doc in enumerate(docs):
    print(f"Chunk {i+1}:\n{doc.page_content}\n")

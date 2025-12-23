# 1. Basic Fixed-Size Chunking
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=2)



raw_text = """
LangChain helps build applications powered by large language models.
Chunking is used in RAG pipelines to split text into smaller pieces.
"""

longer_text = "LangChain helps build applications powered by large language models. " * 5  # ~300 chars


text_splitter = CharacterTextSplitter(
    chunk_size=10,
    chunk_overlap=2,
    
)

docs = text_splitter.create_documents([longer_text])

for i, doc in enumerate(docs, 1):
    print(f"Chunk {i}:")
    print(doc.page_content)
    

# 3. Token-Based Chunking
from langchain_text_splitters import TokenTextSplitter

raw_text = """
Artificial Intelligence is transforming modern software systems.
Large Language Models are trained on massive text corpora and operate
within strict token limits. When building Retrieval-Augmented Generation
systems, documents must be split into token-safe chunks so embeddings
and prompts do not exceed context windows. Token-based chunking ensures
predictable costs and prevents runtime failures caused by token overflow.
"""

text_splitter = TokenTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

docs = text_splitter.create_documents([raw_text])

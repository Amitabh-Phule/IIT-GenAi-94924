# 6. Sentence-Based Chunking (NLP-Style)
from langchain_text_splitters import SentenceTransformersTokenTextSplitter

raw_text = """
Machine learning models learn patterns from data rather than following
explicit rules. In natural language processing, sentences often carry
complete factual meaning. Splitting text at sentence boundaries helps
preserve context and improves the accuracy of question–answering and
information retrieval systems. This approach is especially useful for
short, factual documents and curated Q&A datasets.
"""

text_splitter = SentenceTransformersTokenTextSplitter(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    chunk_size=256,
    chunk_overlap=20
)

docs = text_splitter.create_documents([raw_text])


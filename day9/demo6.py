# 4. Markdown-Aware Chunking
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_text = """
# LangChain Chunking Guide

LangChain provides multiple text splitting strategies to prepare data
for Large Language Models and retrieval systems.

## Character vs Token Chunking

Character-based chunking is simple but unsafe for token-limited models.
Token-based chunking respects model context windows and controls cost.

### When to Use Token Chunking

Use token-based chunking for production RAG pipelines, embeddings,
and any API with strict token limits.

## Markdown-Aware Splitting

Markdown header splitting keeps sections intact and preserves
document structure, making retrieval more accurate.
"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

text_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

docs = text_splitter.split_text(markdown_text)


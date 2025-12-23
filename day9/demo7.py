# 5. Code-Aware Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

code_text = """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
"""

code_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=1000,
    chunk_overlap=100
)

docs = code_splitter.create_documents([code_text])

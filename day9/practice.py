from langchain_text_splitters import (
    CharacterTextSplitter, 
    RecursiveCharacterTextSplitter
)

short_text = """Line1.\n\nLine2."""

# Fixed - specify chunk_overlap explicitly
print("Character:", CharacterTextSplitter(chunk_size=10, chunk_overlap=0).create_documents([short_text]))
print("Recursive:", RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=0).create_documents([short_text]))

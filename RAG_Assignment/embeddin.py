from typing import List
from langchain.embeddings import init_embeddings
import os
from dotenv import load_dotenv

load_dotenv()

embed_model = init_embeddings(
    model="text-embedding-all-minilm-l6-v2-embedding",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key=os.getenv("NOMIC_API_KEY"),
    check_embedding_ctx_length=False
)

def get_embeddings(texts: List[str]) -> List[list[float]]:
    if not texts:
        return []

    vectors = []
    for text in texts:
        if not text.strip():
            continue
        vec = embed_model.embed_documents([text])
        vectors.append(vec[0])

    return vectors

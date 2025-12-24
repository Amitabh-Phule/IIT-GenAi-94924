from langchain.embeddings import init_embeddings

embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="no needed",
    check_embedding_ctx_length=False
)

sentences=[
    "I like Artificial Intelligence",
    "Generative AI is magnificant",
    "World is amazing"
]

embeddings= embed_model.embed_documents(sentences)
for embedding in embeddings:
    print(f"Len = {len(embedding)} --> {embedding[:4]}")
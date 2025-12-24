import chromadb

db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection(name="resumes")

collection.add(
    ids=["resume_id"],
    documents=["This is a sample resume text"],
    metadatas=[{"source": "resume1"}],
    embeddings=[[0.0] * 384]  
)

print("Inserted successfully")
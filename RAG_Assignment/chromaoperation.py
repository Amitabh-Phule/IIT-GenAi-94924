import re
import chromadb
from embeddin import get_embeddings  

db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("resumes")


def add_resume_to_db(resume_id, texts, metadata_list, embeddings):
    """
    Add multiple chunks for a resume.
    - resume_id: string for candidate resume
    - texts: list of chunk strings
    - metadata_list: list of dicts, same length as texts
      each metadata must include at least {'resume_id': resume_id, 'chunk_index': i}
    """
    

    ids = [f"{resume_id}_chunk_{i}" for i in range(len(texts))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadata_list,
        documents=texts,
    )


def search_resumes(query_text, n_results=5):
    if not query_text.strip():
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

    query_embedding = get_embeddings([query_text])[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    return result



def delete_resume_from_db(resume_id):
    """
    Delete all chunks for a given resume_id using metadata filter.
    """
    collection.delete(where={"resume_id": {"$eq": resume_id}})

def get_resume_intro(resume_id):
    results = collection.get(
        where={"resume_id": resume_id}
    )

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    for doc, meta in zip(documents, metadatas):
        if meta.get("chunk_index") == 0:


            lines= doc.splitlines()
            intro=[]

            for line in lines[:3]:
                if(
                    re.search(r"\b\d{10}\b|\+91", line) or
                    "@" in line or
                    "linkedin.com" in line.lower()
                ):
                    intro.append(line.strip())

            return "\n".join(intro).strip()

    return ""

def get_full_resume_text(resume_id):
    """
    Fetch all chunks of a resume and merge them
    while removing overlapping duplicated text.
    """
    results = collection.get(where={"resume_id": resume_id})

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    # Sort by chunk order
    chunks = [
        doc for doc, meta in sorted(
            zip(documents, metadatas),
            key=lambda x: x[1].get("chunk_index", 0)
        )
    ]

    merged_text = ""
    for chunk in chunks:
        merged_text = merge_without_overlap(merged_text, chunk)

    return merged_text

def merge_without_overlap(existing_text, new_chunk, overlap_window=50):
    """
    Merge two texts by removing overlapping suffix/prefix.
    """
    if not existing_text:
        return new_chunk

    # Take last N chars of existing text
    tail = existing_text[-overlap_window:]

    # If overlap found, remove it
    if new_chunk.startswith(tail):
        return existing_text + new_chunk[len(tail):]

    # Fallback: simple append
    return existing_text + "\n" + new_chunk










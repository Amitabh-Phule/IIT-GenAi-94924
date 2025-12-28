import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from chromaoperation import collection

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage


from pdfoperation import load_pdf_resume, split_resume_text
from embeddin import get_embeddings
from chromaoperation import (
    add_resume_to_db,
    search_resumes,
    get_resume_intro,
    delete_resume_from_db,
    get_full_resume_text,
)


load_dotenv()

if "llm" not in st.session_state:
    st.session_state.llm = init_chat_model(
        model="openai/gpt-oss-120b",
        model_provider="openai",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
    )

llm = st.session_state.llm


if "resumes" not in st.session_state:
    st.session_state.resumes = []

if "show_manage" not in st.session_state:
    st.session_state.show_manage = False

if "show_all_resumes" not in st.session_state:
    st.session_state.show_all_resumes = False


def deduplicate_and_rank(docs, metas, dists):
    seen_resumes = set()
    unique_results = []

    for doc, meta, dist in zip(docs, metas, dists):
        resume_id = meta.get("resume_id")
        if not resume_id:
            continue
        if resume_id in seen_resumes:
            continue

        seen_resumes.add(resume_id)
        unique_results.append({
            "doc": doc,
            "meta": meta,
            "dist": dist
        })

    return unique_results


def explain_match(job_description: str, full_resume_text: str) -> str:
    messages = [
        SystemMessage(
            content=(
                "You are an HR AI assistant. "
                "Analyze the full resume against the job description "
                "and explain the candidate's suitability."
            )
        ),
        HumanMessage(
            content=(
                f"Job Description:\n{job_description}\n\n"
                f"Full Resume:\n{full_resume_text}\n\n"
                "Give a concise evaluation in 4–5 bullet points, "
                "and give the final recommendation for the best candidate."
            )
        ),
    ]

    response = llm.invoke(messages)
    return response.content


st.set_page_config(
    page_title="AI Resume Shortlisting System",
    layout="wide",
)

st.title("AI Resume Shortlisting System")
st.caption(
    "Upload resumes, index them using embeddings + ChromaDB, "
    "and shortlist candidates with AI explanations."
)


with st.sidebar:
    st.header("Resume Management")

    with st.form("index_resume_form"):
        uploaded_pdf = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"]
        )
        submit_index = st.form_submit_button("Index Resume")

    if submit_index:
        if not uploaded_pdf:
            st.warning("Please upload a resume first.")
        else:
            with st.spinner("Indexing resume..."):
                temp_path = f"./temp_{uploaded_pdf.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_pdf.getbuffer())

                resume_text, meta = load_pdf_resume(temp_path)
                chunks = split_resume_text(resume_text)

                texts = [f"search_document: {c}" for c in chunks]
                embeddings = get_embeddings(texts)

                resume_id = Path(uploaded_pdf.name).stem

                metadatas = [
                    {
                        "resume_id": resume_id,
                        "source": meta["source"],
                        "page_count": meta["page_count"],
                        "chunk_index": i,
                    }
                    for i in range(len(chunks))
                ]

                add_resume_to_db(
                    resume_id=resume_id,
                    texts=chunks,
                    metadata_list=metadatas,
                    embeddings=embeddings,
                )

                st.session_state.resumes.append(
                    {"resume_id": resume_id, "source": meta["source"]}
                )

                st.success(f"Resume **{resume_id}** indexed successfully.")

    if st.button("Manage Resumes", use_container_width=True):
        st.session_state.show_manage = not st.session_state.show_manage
        st.rerun()

    if st.button("View All Resumes", use_container_width=True):
        st.session_state.show_all_resumes = True
        st.rerun()

#manage resumes section
if st.session_state.show_manage:
    st.subheader("Indexed Resumes")

    if not st.session_state.resumes:
        st.info("No resumes indexed yet.")
    else:
        for i, resume in enumerate(st.session_state.resumes):

            col1, col2 = st.columns([5, 1])

            with col1:
                st.write(
                    f"**Resume ID:** {resume['resume_id']}  \n"
                    f"**Source:** {resume['source']}"
                )

            with col2:
                if st.button("Delete", key=f"delete_{resume['resume_id']}_{i}"):

                    delete_resume_from_db(resume["resume_id"])
                    st.session_state.resumes.remove(resume)
                    st.success("Resume deleted.")
                    st.rerun()


if st.session_state.show_all_resumes:
    st.subheader("All Resumes in Database")

    try:
        all_data = collection.get()
        metas = all_data.get("metadatas", [])

        if not metas:
            st.info("No resumes found in database.")
        else:
            seen = set()
            for meta in metas:
                rid = meta.get("resume_id")
                if rid and rid not in seen:
                    seen.add(rid)
                    st.write(f"Resume ID: {rid}")
    except Exception as e:
        st.error(str(e))

st.divider()


st.subheader("Shortlist Candidates")

with st.form("shortlist_form"):
    job_description = st.text_area(
        "Paste Job Description",
        height=220,
    )

    max_results = st.slider(
        "Number of candidates to shortlist",
        min_value=1,
        max_value=20,
        value=5,
    )

    submit_shortlist = st.form_submit_button("Shortlist Candidates")

if submit_shortlist:
    if not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        try:
            results = search_resumes(
                job_description,
                n_results=max_results * 15
            )

            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]

            grouped_results = deduplicate_and_rank(docs, metas, dists)
            final_results = grouped_results[:max_results]

            if not final_results:
                st.info("No matching resumes found.")
            else:
                for i, item in enumerate(final_results, start=1):
                    resume_id = item["meta"]["resume_id"]
                    dist = item["dist"]

                    st.subheader(f"Candidate Match {i}")
                    st.write(f"Resume ID: {resume_id}")
                    st.write(f"Relevance Score: {1 - dist:.2f}")

                    with st.expander("Candidate Contact & Profile"):
                        st.write(get_resume_intro(resume_id) or "Not available")

                    with st.expander("Matching Skills / Experience"):
                        st.write(get_full_resume_text(resume_id))

                    with st.expander("AI Explanation"):
                        st.write(
                            explain_match(
                                job_description,
                                get_full_resume_text(resume_id)
                            )
                        )

        except Exception as e:
            st.error(str(e))

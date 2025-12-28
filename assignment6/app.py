# Design a Streamlit-based application with a sidebar to switch between Groq and LM Studio.
# The app should accept a user question and display responses using Groq’s cloud LLM and a locally running LM Studio model.
# Also maintain and display the complete chat history of user questions and model responses.

import streamlit as st
import requests
import os
import re
from dotenv import load_dotenv

# ---------- CONFIG ----------
st.set_page_config(page_title="Chat Bot", layout="wide")
st.title("🤖 My ChatBot")

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

# ---------- UTILS ----------
def remove_think_tags(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("⚙ Settings")

    model_choice = st.radio(
        "Choose LLM Model:",
        ("Groq (Cloud)", "LM Studio (Local)")
    )

    st.divider()
    st.subheader("🕘 Complete Chat History")

    if st.session_state.messages:
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "Bot"
            st.write(f"**{role}:** {msg['content']}")
    else:
        st.write("No conversation yet.")

    if st.button("🗑 Clear History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("ℹ Info")
    st.write("""
    - Groq: Cloud-based LLM
    - LM Studio: Local LLM
    - Full chat history is preserved
    """)

# ---------- MAIN CHAT DISPLAY ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------- USER INPUT ----------
user_input = st.chat_input("Ask anything...")

# ---------- MODEL CALLS ----------
def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(GROQ_URL, json=data, headers=headers)
    raw = res.json()["choices"][0]["message"]["content"]
    return remove_think_tags(raw)

def call_lmstudio(prompt):
    data = {
        "model": "microsoft/phi-4-mini-reasoning",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(LMSTUDIO_URL, json=data)
    raw = res.json()["choices"][0]["message"]["content"]
    return remove_think_tags(raw)

# ---------- HANDLE CHAT ----------
if user_input:
    # Store & display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

    # Get model reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if model_choice == "Groq (Cloud)":
                reply = call_groq(user_input)
            else:
                reply = call_lmstudio(user_input)
            st.write(reply)

    # Store assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

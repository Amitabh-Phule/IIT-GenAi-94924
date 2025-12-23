import os
import requests
import json
from dotenv import load_dotenv
import streamlit as st

st.title("My Chatbot")

load_dotenv()

api_key = "dummy-key"  # LM Studio ignores this, but header is required
url = "http://127.0.0.1:1234/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# ---- INPUT ----
user_prompt = st.text_input("Ask anything:")

# ---- CALL API ----
if user_prompt:
    req_data = {
        "model": "microsoft/phi-4-mini-reasoning",
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(url, json=req_data, headers=headers)
    resp = response.json()

    st.write(resp["choices"][0]["message"]["content"])

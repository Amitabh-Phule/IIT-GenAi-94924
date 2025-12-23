import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

st.title("Langchain ChatBot")

llm = init_chat_model(
    model = "openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

user_input = st.chat_input("say something...")
if user_input:
    result = llm.stream(user_input)
    # msg_box = st.empty()
    # output=""
    # for chunk in result:
    #     output += chunk.content
    #     msg_box.markdown(output)
    st.write_stream([chunk.content for chunk in result])
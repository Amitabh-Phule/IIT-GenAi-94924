import streamlit as st
import time

st.set_page_config(page_title="Chat Bot", layout="wide")
st.title("My ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("📌 Sidebar")

    # History
    st.subheader("🕘 History")
    if st.session_state.messages:
        for role, msg in st.session_state.messages:
            st.write(f"{role.capitalize()}: {msg}")
    else:
        st.write("No chat history yet.")

    if st.button("🗑 Clear History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    #ChatGPT_info
    st.subheader("🤖 ChatGPT Info")
    st.write("""
    - ChatGPT is an AI chatbot  
    - Built using Large Language Models (LLMs)  
    - Can answer questions & chat naturally  
    - Used in apps, assistants & chat systems  
    """)

#Display_chat_history
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

#User_Input
user_input = st.chat_input("Type your message")

if user_input:
    # Store_user_message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    
    bot_reply = f"You said: {user_input}"
    def stream_reply(text):
        for word in text.split():
            yield word + " "
            time.sleep(0.3)

    with st.chat_message("assistant"):
        st.write_stream(stream_reply(bot_reply))

    st.session_state.messages.append(("assistant", bot_reply))

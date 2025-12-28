# • Create two tools using the @tool decorator: a CSV Question Answering tool and a Web Scraping tool.
# • The CSV tool should upload a CSV file, show its schema, and answer user questions by converting them into SQL queries using pandasql.
# • The Web Scraping tool should collect internship and batch information from the Sunbeam Institute website and answer related queries.
# • Build a single intelligent agent that automatically selects and uses the correct tool based on the user’s question.
# • Test the agent with relevant prompts, inspect message history to observe tool-calling behavior, maintain full chat history, and explain all responses in simple English.

import streamlit as st
import pandas as pd
import pandasql as ps
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

load_dotenv()

# ------------------- LLM INITIALIZATION -------------------
llm = init_chat_model(
    model="google/gemma-3n-e4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ------------------- SESSION STATE -------------------
if "sql_history" not in st.session_state:
    st.session_state.sql_history = []

if "scrape_history" not in st.session_state:
    st.session_state.scrape_history = []

if "scraped_df" not in st.session_state:
    st.session_state.scraped_df = None

# ------------------- TOOLS -------------------

@tool
def sql_agent(prompt: str):
    """
    SQL Agent Tool
    Takes a CSV path and a question (format: "file.csv : question"),
    generates SQL query, executes it, and provides result and explanation.
    """
    try:
        path, question = prompt.split(":", 1)
        path = path.strip()
        question = question.strip()
    except:
        return "Invalid format. Use: file.csv : your question"

    df = pd.read_csv(path)

    # Generate SQL query
    sql_prompt = f"""
    You are an expert SQL developer.
    Table name: data
    Schema: {df.dtypes}
    Question: {question}
    Generate ONLY a valid SQLite SQL query. No markdown, no backticks.
    """
    raw_query = llm.invoke(sql_prompt).content.strip()
    query = raw_query.replace("sql", "").replace("", "").replace("`", "").strip()

    # Execute SQL
    try:
        result = ps.sqldf(query, {"data": df})
    except Exception as e:
        return f"SQL Execution Failed:\nQuery: {query}\nError: {str(e)}"

    # Explain result
    explain_prompt = f"""
    Explain the following SQL query result in short sentences.

    SQL Query: {query}
    Result: {result}
    """
    explanation = llm.invoke(explain_prompt).content.strip()

    return f"SQL Query:\n{query}\n\nResult:\n{result}\n\nExplanation:\n{explanation}"


@tool
def web_scrape(query: str):
    """
    Web Scraping Tool
    Scrapes internship batch data from sunbeaminfo.in.
    Uses cached table if already scraped.
    Answers user questions in short summary sentences.
    """
    # Scrape only if table not already in session
    if st.session_state.scraped_df is None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.sunbeaminfo.in/internship")
        driver.implicitly_wait(10)

        table = driver.find_element(By.CLASS_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        data_list = []
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            data_list.append({
                "sr": cols[0].text,
                "batch": cols[1].text,
                "duration": cols[2].text,
                "start": cols[3].text,
                "end": cols[4].text,
                "time": cols[5].text,
                "fees": cols[6].text,
                "brochure": cols[7].text
            })

        driver.quit()

        st.session_state.scraped_df = pd.DataFrame(data_list)

    # Use existing table to answer question
    if query.strip():
        prompt = f"""
        You are a data analyst.
        Here is the internship table data: {st.session_state.scraped_df.to_string()}
        Question: {query}
        Answer in 3-5 short sentences. Summarize. No tables unless explicitly requested.
        """
        answer = llm.invoke(prompt).content.strip()
        return answer

    return "Web scraping completed. Data is ready."


# ------------------- STREAMLIT UI -------------------
st.title("🧠 Multi-Agent System")
st.caption(
    "This app provides two AI-powered agents:\n"
    "- 📊 SQL Query Agent: Ask questions on CSV data using natural language\n"
    "- 🌐 Web Scraping Agent: Ask questions on scraped internship data"
    )

tool_choice = st.sidebar.selectbox("Select Tool", ["SQL Query Agent", "Web Scraping Agent"])

# ------------------- SQL TOOL UI -------------------
if tool_choice == "SQL Query Agent":
    st.header("📊 SQL Query Agent")

    data_file = st.file_uploader("Upload CSV file", type=["csv"])
    if data_file:
        df = pd.read_csv(data_file)
        st.dataframe(df)

        # Display previous chat
        for msg in st.session_state.sql_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # User input
        user_input = st.chat_input("Ask a question about CSV data…")
        if user_input:
            st.session_state.sql_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            path = "temp.csv"
            df.to_csv(path, index=False)
            prompt = f"{path} : {user_input}"

            result = sql_agent.run(prompt)
            st.session_state.sql_history.append({"role": "assistant", "content": result})
            with st.chat_message("assistant"):
                st.write(result)

# ------------------- WEB SCRAPING TOOL UI -------------------
elif tool_choice == "Web Scraping Agent":
    st.header("🌐 Web Scraping Agent")

    # Display previous chat
    for msg in st.session_state.scrape_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User question
    question = st.chat_input("Ask a question about scraped data…")
    if question:
        st.session_state.scrape_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        answer = web_scrape.run(question)
        st.session_state.scrape_history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)

    # Display scraped table if available
    if st.session_state.scraped_df is not None:
        st.subheader("Scraped Internship Data")
        st.dataframe(st.session_state.scraped_df)
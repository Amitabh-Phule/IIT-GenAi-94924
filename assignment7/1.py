# Create a Streamlit application that allows users to upload a CSV file and view its schema.
# Use an LLM to convert user questions into SQL queries, execute them on the CSV data using pandasql, and explain the results in simple English.


import streamlit as st
import pandas as pd
from pandasql import sqldf
from groq import Groq
import os
from dotenv import load_dotenv

# -------------------- Setup --------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Ask Your CSV", layout="centered")

# -------------------- Header --------------------
st.markdown("## Ask Your CSV")
st.caption("Upload a CSV file and ask questions in plain English.")

st.markdown("---")

# -------------------- Upload --------------------
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if not uploaded_file:
    st.info("👆 Upload a CSV file to get started.")
    st.stop()

df = pd.read_csv(uploaded_file)

# -------------------- Schema --------------------
with st.expander("View column information"):
    schema = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.astype(str)
    })
    st.table(schema)

# -------------------- Ask Question --------------------
st.markdown("### What would you like to know?")
user_question = st.text_input(
    label="",
)

if not user_question:
    st.stop()

st.markdown("---")

# -------------------- SQL Generation --------------------
with st.spinner("Thinking..."):
    sql_prompt = f"""
You are an expert SQL assistant.

Table name: df

Schema:
{schema.to_string(index=False)}

Convert the user question into a valid SQLite SQL query.
Return ONLY the SQL query.

Question:
{user_question}
"""
    sql_response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": sql_prompt}],
        temperature=0.0
    )

sql_query = sql_response.choices[0].message.content.strip()

# -------------------- SQL Execution --------------------
try:
    result = sqldf(sql_query, {"df": df})
except Exception as e:
    st.error("I couldn't answer that question using the data.")
    st.caption("Try rephrasing your question.")
    st.stop()

# -------------------- Result --------------------
st.markdown("### Result")
st.dataframe(result, use_container_width=True)

# -------------------- Explanation --------------------
with st.spinner("Explaining the result..."):
    explain_prompt = f"""
Explain the following result in simple English.

Question:
{user_question}

Result:
{result.head(10).to_string(index=False)}
"""
    explanation_response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": explain_prompt}],
        temperature=0.0
    )

st.markdown("### Explanation")
st.write(explanation_response.choices[0].message.content)

# -------------------- Advanced --------------------
with st.expander("Advanced: View generated SQL"):
    st.code(sql_query, language="sql")

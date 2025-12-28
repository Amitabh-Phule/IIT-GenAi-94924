# Create a Streamlit application that takes a city name as input from the user.
# Fetch the current weather using a Weather API and use an LLM to explain the weather conditions in simple English.

import streamlit as st
import requests
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(page_title="Weather App", page_icon="🌦")

# ---------------- LOAD ENV ----------------
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# ---------------- INIT LLM ----------------
llm = init_chat_model(
    model="google/gemma-3n-e4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy"
)

# ---------------- WEATHER FUNCTION ----------------
def Weather():
    with st.form("weather_form"):
        city = st.text_input("Enter city name")
        submitted = st.form_submit_button("Get Weather")

    if not submitted:
        return

    if not city:
        st.warning("Please enter a city name")
        return

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
    )
    response = requests.get(url)

    if response.status_code != 200:
        st.error("City not found or API error")
        return

    data = response.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"]

    llm_msg = f"""
    Weather details:
    Temperature: {temp} °C
    Humidity: {humidity} %
    Wind Speed: {wind} m/s
    Condition: {description}

    Explain the weather in simple bullet points for a normal user.
    """

    result = llm.invoke(llm_msg)

    st.subheader("🌤 Current Weather")
    st.write(f"**Temperature:** {temp} °C")
    st.write(f"**Humidity:** {humidity} %")
    st.write(f"**Wind Speed:** {wind} m/s")
    st.write(f"**Condition:** {description}")

    st.subheader("🤖 AI Explanation")
    st.write(result.content)

# ---------------- SESSION STATE ----------------
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- UI ----------------
if not st.session_state.login:
    st.title("🔐 Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == password and user != "":
            st.session_state.login = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

else:
    st.title("🌦 Weather Application")

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

    Weather()

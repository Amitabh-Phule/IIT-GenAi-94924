import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")


if not api_key:
    st.error("API key not found. Check your .env file.")

# --------- SESSION STATE ---------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "thanks" not in st.session_state:
    st.session_state.thanks = False

# --------- LOGIN PAGE ---------
def login_page():
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == pwd and user != "":
            st.session_state.logged_in = True
            st.session_state.thanks = False
            st.success("Login Successful")
        else:
            st.error("Invalid Login")

# --------- WEATHER PAGE ---------
def weather_page():
    st.title("🌦 Weather App")

    city = st.text_input("Enter city name")

    if st.button("Get Weather", key="get_weather"):
        if not city.strip():
            st.warning("City name cannot be empty")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city.strip()}"

        try:
            res = requests.get(url, timeout=10)
            data = res.json()

            if data.get("cod") == 200:
                st.subheader(f"{data['name']}, {data['sys']['country']}")
                st.metric("🌡 Temperature (°C)", data["main"]["temp"])
                st.metric("💧 Humidity (%)", data["main"]["humidity"])
                st.write("☁ Condition:", data["weather"][0]["description"].capitalize())
                st.write(f"🌬 Wind Speed: {data['wind']['speed']} m/s")
            else:
                st.error(data.get("message", "City not found"))

        except Exception as e:
            st.error("Network error. Try again later.")

    if st.button("Logout", key="logout"):
        st.session_state.logged_in = False
        st.session_state.thanks = True

# --------- THANK YOU PAGE ---------
def thanks_page():
    st.title("🙏 Thanks for using the app")

# --------- PAGE CONTROLLER ---------
if st.session_state.logged_in:
    weather_page()
elif st.session_state.thanks:
    thanks_page()
else:
    login_page()

import streamlit as st
import requests
import os
import dotenv as dt


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "logout" not in st.session_state:
    st.session_state.logout = False


def login_page():
    st.title("🔐 Login Page")

    username = st.text_input("username")
    password = st.text_input("password", type="password")

    if st.button("Login"):
        if username and password and username == password:
            st.session_state.logged_in = True
            st.session_state.logout = False
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Login (Username must be same as Password)")


def weather_page():
    st.title("🌦️ Weather Application")

    city = st.text_input("Enter City Name")
    dt.load_dotenv()
    API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

    if st.button("Get Weather"):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            print("status:", response.status_code)

            if response.status_code == 200:
                data = response.json()

                st.subheader(f"🌍 Weather in {city}")
                st.write(f"Temperature: {data['main']['temp']} °C")
                st.write(f"Condition: {data['weather'][0]['description'].title()}")
                st.write(f"Humidity: {data['main']['humidity']}%")
                st.write(f"Wind Speed: {data['wind']['speed']} m/s")
            else:
                st.error("City not found or invalid API key")
        else:
            st.warning("Please enter a city name")

    st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.logout = True
        st.rerun()


def thank_you_page():
    st.title("✅ Thank You")
    st.success("Thank you for using the Weather Application!")


if st.session_state.logged_in:
    weather_page()
elif st.session_state.logout:
    thank_you_page()
else:
    login_page()

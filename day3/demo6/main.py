import streamlit as st

st.title("Sunbeam Infotech")

# ---- Page Functions ----
def show_aboutus_page():
    st.header("About Us")
    st.write(
        "At Sunbeam we believe retaining a competitive edge is imperative for any individual "
        "in today's professional world."
    )

def show_internship_page():
    st.header("Internship")
    st.write(
        "Technology, innovations and business trends have added diversified change "
        "to organizational processes."
    )

def show_courses_page():
    st.header("Courses")

def show_contactus_page():
    st.header("Contact Us")
    st.markdown("### Sunbeam Hinjewadi")
    st.write(
        '"Sunbeam IT Park", Second Floor, Phase 2 of Rajiv Gandhi Infotech Park, '
        'Hinjawadi, Pune - 411057, MH-INDIA'
    )

# ---- Session State Initialization ----
if "page" not in st.session_state:
    st.session_state.page = "About Us"

# ---- Sidebar Navigation ----
with st.sidebar:
    if st.button("About Us", use_container_width=True):
        st.session_state.page = "About Us"
    if st.button("Internship", use_container_width=True):
        st.session_state.page = "Internship"
    if st.button("Courses", use_container_width=True):
        st.session_state.page = "Courses"
    if st.button("Contact Us", use_container_width=True):
        st.session_state.page = "Contact Us"

# ---- Page Routing ----
if st.session_state.page == "About Us":
    show_aboutus_page()
elif st.session_state.page == "Internship":
    show_internship_page()
elif st.session_state.page == "Courses":
    show_courses_page()
elif st.session_state.page == "Contact Us":
    show_contactus_page()

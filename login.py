import streamlit as st
from utils import render_goodwill_header

def login_page():
    render_goodwill_header()  # Assuming this function renders the company logo


    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Handle login attempt
    if st.button("Login"):
        # Dummy logic to simulate login
        if username == "admin" and password == "admin":
            st.session_state.page = "home"  # Set the page to "home" when login is successful
            st.session_state.logged_in = True  # Set logged_in flag to True
            st.rerun()  # Reload the app to navigate to the home page
        else:
            st.error("Invalid username or password.")

    # Registration button to redirect to the registration page
    if st.button("Go to Registration"):
        st.session_state.page = "register"  # Set the page to "register" for registration
        st.rerun()  # Reload the app to navigate to the registration page

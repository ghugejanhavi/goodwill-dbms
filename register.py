import streamlit as st
from utils import render_goodwill_header
from database import insert_user  # Import the insert_user function

def register_page():
    render_goodwill_header()  # Assuming this function renders the company logo

    st.title("Register")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if password != confirm_password:
        st.error("Passwords do not match.")

    elif st.button("Register"):
        # Check if the user already exists in the database (Optional)
        # You can implement a check here, for example:
        # if check_user_exists(username):
        #     st.error("Username already exists.")
        #     return

        # Insert the new user into the database
        success = insert_user(username, password)
        st.write("Hello, this is some text! success,", success)

        if success:
            st.success("Registration successful! Redirecting to login.")
            st.session_state.page = "login"  # After registration, go back to the login page
            st.experimental_rerun()  # Trigger rerun to redirect to login page
        else:
            st.error("Registration failed. Please try again later.")

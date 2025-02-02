import streamlit as st
from login import login_page
from register import register_page
from home import home_page
from donations import donations_page
from events import events_page
from employees import employees_page
from analytics_page import analytics_page

# Check if the user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Define the page mapping for each page function
page_mapping = {
    "login": login_page,
    "register": register_page,
    "home": home_page,
    "donations": donations_page,
    "events": events_page,
    "employees": employees_page,
    "analytics":analytics_page
}

# Set the initial page to "login" if not already set
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default to login page

# Check if the user is logged in
if st.session_state.logged_in:
    # If the user is logged in, set the page to "home"
    if st.session_state.page == "login":
        st.session_state.page = "home"  # Redirect to home page after login

# Trigger the page render based on session_state.page
page_mapping[st.session_state.page]()  # Display the appropriate page function

import streamlit as st
from utils import render_goodwill_header

def home_page():
    render_goodwill_header()
    
    # Set up the sidebar with the navigation options and logout button
    st.sidebar.title('HOME')
    
    # Default option will be a prompt to choose a page
    nav_items = {
        "Select a service": None,  # Default prompt, no page selected
        "Donations": "donations",
        "Events": "events",
        "Employees": "employees",
        "Reports and Analytics": "analytics"  # New Reports and Analytics page
    }

    # Display the navigation options in the sidebar using a selectbox
    selected_page = st.sidebar.selectbox("Choose a service:", list(nav_items.keys()))

    # Redirect to the selected page
    if selected_page == "Donations":
        st.session_state.page = "donations"
        st.experimental_rerun()
    elif selected_page == "Events":
        st.session_state.page = "events"
        st.experimental_rerun()
    elif selected_page == "Employees":
        st.session_state.page = "employees"
        st.experimental_rerun()
    elif selected_page == "Reports and Analytics":
        st.session_state.page = "analytics"
        st.experimental_rerun()
    elif selected_page == "Select a service":
        st.sidebar.write("Please choose an option from the sidebar.")

    # Add a logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.experimental_rerun()

    # If no navigation is selected, render the home page with a prompt to choose a page
    if "page" not in st.session_state or st.session_state.page == "home":
        st.write("Welcome to the Home Page! Please choose an option from the sidebar.")

    # Ensure the right page is displayed based on session state
    if st.session_state.page == "donations":
        donations_page()  # Define in your project
    elif st.session_state.page == "events":
        events_page()  # Define in your project
    elif st.session_state.page == "employees":
        employees_page()  # Define in your project
    elif st.session_state.page == "analytics":
        analytics_page()  # New analytics page

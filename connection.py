import oracledb
import streamlit as st

def init_oracle_client():
    """Initialize the Oracle Client for thick mode."""
    try:
        oracledb.init_oracle_client()  # Initializes the Oracle client
        st.write("Oracle client initialized successfully!")
    except Exception as e:
        st.error(f"Error initializing Oracle client: {e}")

connection = oracledb.connect(user="mis531groupS2M", password="b4M65[No!6{BMvL",
                              host="navydb.artg.arizona.edu", port=1521, service_name="COMPDB",disable_oob= True)
print("Hello, connection is some text!,", connection)

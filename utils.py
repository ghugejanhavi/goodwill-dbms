import streamlit as st
import oracledb
import pandas as pd

oracledb.init_oracle_client(lib_dir=r"C:\Users\ual-laptop\Documents\instantclient\instantclient_23_6")

# Configure Oracle DB connection
def connect_to_db():
    return oracledb.connect(user="mis531groupS2M", password="b4M65[No!6{BMvL",
                              host="navydb.artg.arizona.edu", port=1521, service_name="COMPDB",disable_oob= True)

# Utility function to render header
def render_goodwill_header():
    col1, col2 = st.columns([1, 3])  # Adjust column widths if needed

    with col1:
        # Display the logo in the first column
        st.image("logo.png", width=80)  # Adjust the width of the logo

    with col2:
        # Display the company name "GOODWILL"
        st.markdown("""
            <h1 style="font-size:50px; color:#007bff; font-weight:bold;">GOODWILL</h1>
        """, unsafe_allow_html=True)
    
    st.markdown(""" 
        <style>
        .logout-btn {
            position: fixed;
            top: 10px;
            right: 20px;
            background-color: #ff4d4d;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .logout-btn:hover {
            background-color: #ff1a1a;
        }
        </style>
    """, unsafe_allow_html=True)

# # Utility function to execute queries
# def run_query(query, params=None):
#     with connect_to_db() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(query, params or [])
#             conn.commit()
#             return cursor.fetchall()  # Fetch and return the result if needed

def run_query(query, params=None):
    try:
        with connect_to_db() as conn:  # Replace `db_connection` with your connection logic
            cursor = conn.cursor()
            cursor.execute(query, params or {})

            if query.strip().lower().startswith("select"):
                return cursor.fetchall()  # For SELECT queries, return fetched results

            conn.commit()  # For non-SELECT queries (INSERT, UPDATE, DELETE)
            return None  # No rows to return for these queries
    except Exception as e:
        raise e

import oracledb
import streamlit as st

def get_oracle_connection():
    try:
        # Initialize Oracle client (if needed)
        oracledb.init_oracle_client(lib_dir=r"C:\Users\ual-laptop\Documents\instantclient\instantclient_23_6")

        # Connect to the Oracle database
        connection = oracledb.connect(
            user="mis531groupS2M", 
            password="b4M65[No!6{BMvL",
            host="navydb.artg.arizona.edu", 
            port=1521, 
            service_name="COMPDB"
        )
        
        st.write("Connection successful!")
        return connection

    except Exception as e:
        print(f"Error while connecting to Oracle: {e}")
        return None


def insert_user(username, password):
    conn = get_oracle_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Insert the new user into the 'users' table using parameterized query
            st.write("User successfully before!", username, password)
            cursor.execute(
    "INSERT INTO USERS (username, password) VALUES (:1, :2)",
    (username, password)
)


            conn.commit()  # Commit the changes
            st.write("User successfully inserted!")
            return True
        except Exception as e:
            print(f"Error while inserting user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        return False

import streamlit as st
import pandas as pd
from utils import run_query, render_goodwill_header

def employees_page():
    # Initialize session state flags if they don't exist
    if "submit_e_button" not in st.session_state:
        st.session_state.submit_e_button = False
    if "update_button_clicked" not in st.session_state:
        st.session_state.update_button_clicked = False
    
    # Create columns for the header and the "Back to Home" button
    col1, col2 = st.columns([5, 1])  # First column takes more space for the header, second column for button

    with col1:
        # Render the company header (logo and title)
        render_goodwill_header()

    with col2:
        # Place the "Back to Home" button in the right column
        if st.button("Back"):
            st.session_state.page = "home"
            st.experimental_rerun()

    st.header("Employees Management")

    action = st.selectbox("Action", ["Create", "View"])

    if action == "Create":
        with st.form("employee_form"):
            emp_firstname = st.text_input("First Name")
            emp_lastname = st.text_input("Last Name")
            emp_email = st.text_input("Email")
            emp_phone = st.text_input("Phone Number")
            emp_street = st.text_input("Street Address")
            emp_state = st.text_input("State")
            emp_zip = st.text_input("ZIP Code")
            emp_hire_date = st.date_input("Hire Date")
            emp_type = st.selectbox("Employee Type", ["Manager", "Worker", "Delivery Partner"])

            # Submit the form
            submitted = st.form_submit_button("Submit", on_click=callback)

            if submitted:
                try:
                    run_query(
                        """
                        INSERT INTO employees (
                            emp_firstname, emp_lastname, emp_email_id, emp_phone_num, emp_street,
                            emp_state, emp_zip, emp_hire_date, emp_type
                        )
                        VALUES (
                            :emp_firstname, :emp_lastname, :emp_email, :emp_phone, :emp_street,
                            :emp_state, :emp_zip, :emp_hire_date, :emp_type
                        )
                        """,
                        {
                            "emp_firstname": emp_firstname,
                            "emp_lastname": emp_lastname,
                            "emp_email": emp_email,
                            "emp_phone": emp_phone,
                            "emp_street": emp_street,
                            "emp_state": emp_state,
                            "emp_zip": emp_zip,
                            "emp_hire_date": emp_hire_date,
                            "emp_type": emp_type,
                        }
                    )
                    st.success("Employee added successfully!")
                except Exception as e:
                    st.error(f"Error adding employee: {e}")
    
    elif action == "View":
        def display_employee_table():
            try:
                results = run_query("SELECT * FROM employees")
                
                if results:
                    df = pd.DataFrame(results, columns=[ 
                        "EID", "Hire Date", "First Name", "Last Name", "Email", "Street",
                        "State", "ZIP", "Phone Number", "Employee Type"
                    ])
                    st.dataframe(df)  # Display the employee table
                    return df
                else:
                    st.write("No employees found.")
                    return None
            except Exception as e:
                st.error(f"Error fetching employees: {e}")
                return None

        df = display_employee_table()

        if df is not None and not df.empty:
            # Add delete option
            # row_to_delete = st.text_input("Enter Employee ID to Delete")
            # if st.button("Delete") and row_to_delete:
            #     try:
            #         run_query("DELETE FROM employees WHERE eid = :eid", {"eid": row_to_delete})
            #         st.success("Employee deleted successfully!")
            #         st.experimental_rerun()  # Refresh the table
            #     except Exception as e:
            #         st.error(f"Error deleting employee: {e}")

            # Add update option
            row_to_update = st.text_input("Enter Employee ID to Update")
            if row_to_update:
                # Fetch employee data by ID
                emp_row = run_query("SELECT * FROM employees WHERE eid = :eid", {"eid": row_to_update})

                if emp_row:
                    if len(emp_row[0]) == 10:  # Adjust this length based on your DB schema
                        # Initialize form for update
                        with st.form("update_form"):
                            updated_firstname = st.text_input("First Name", value=emp_row[0][2])
                            updated_lastname = st.text_input("Last Name", value=emp_row[0][3])
                            updated_email = st.text_input("Email", value=emp_row[0][4])
                            updated_phone = st.text_input("Phone Number", value=emp_row[0][8])
                            updated_street = st.text_input("Street Address", value=emp_row[0][5])
                            updated_state = st.text_input("State", value=emp_row[0][6])
                            updated_zip = st.text_input("ZIP Code", value=emp_row[0][7])
                            updated_hire_date = st.date_input("Hire Date", value=pd.to_datetime(emp_row[0][1]))
                            updated_type = st.selectbox("Employee Type", ["Manager", "Worker", "Delivery Partner"], 
                                                        index=["Manager", "Worker", "Delivery Partner"].index(emp_row[0][9]))
                            
                            # Submit button for update
                            update_submitted = st.form_submit_button("Save Update", on_click=callback_2)

                            if update_submitted:
                                try:
                                    run_query(
                                        """
                                        UPDATE employees 
                                        SET emp_firstname = :emp_firstname, emp_lastname = :emp_lastname,
                                            emp_email_id = :emp_email, emp_phone_num = :emp_phone,
                                            emp_street = :emp_street, emp_state = :emp_state, emp_zip = :emp_zip,
                                            emp_hire_date = :emp_hire_date, emp_type = :emp_type
                                        WHERE eid = :eid
                                        """,
                                        {
                                            "eid": row_to_update,
                                            "emp_firstname": updated_firstname,
                                            "emp_lastname": updated_lastname,
                                            "emp_email": updated_email,
                                            "emp_phone": updated_phone,
                                            "emp_street": updated_street,
                                            "emp_state": updated_state,
                                            "emp_zip": updated_zip,
                                            "emp_hire_date": updated_hire_date,
                                            "emp_type": updated_type,
                                        }
                                    )
                                    st.success("Employee updated successfully!")
                                    st.experimental_rerun()  # Refresh the table
                                except Exception as e:
                                    st.error(f"Error updating employee: {e}")
                    else:
                        st.error("Employee data is not in the expected format.")
                else:
                    st.error("Employee ID not found.")

# Callback function to update the state for form submission
def callback():
    st.session_state.submit_e_button = True

# Callback function to handle the update submission
def callback_2():
    st.session_state.update_button_clicked = True

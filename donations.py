import streamlit as st
import pandas as pd
from utils import run_query, render_goodwill_header

def donations_page():
    # Create columns for the header and "Back" button
    col1, col2 = st.columns([5, 1])

    with col1:
        render_goodwill_header()

    with col2:
        if st.button("Back"):
            st.session_state.page = "home"
            st.experimental_rerun()

    st.header("Donations Management")

    action = st.selectbox("Action", ["Create", "View"])

    if action == "Create":
        # Donor Type Selection Outside Form
        donor_status = st.selectbox("Are you an existing or new donor?", ["Select", "Existing Donor", "New Donor"])

        if donor_status == "New Donor":
            with st.expander("Enter New Donor Details"):
                email = st.text_input("Email ID")
                phone = st.text_input("Phone Number")
                street = st.text_input("Street Address")
                state = st.text_input("State")
                zip_code = st.text_input("ZIP Code")
                donor_type = st.selectbox("Donor Category", ["INDV", "ORG"])

                if donor_type == "INDV":
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    age = st.number_input("Age", min_value=1, max_value=120, step=1)
                    gender = st.selectbox("Gender", ["M", "F", "O"])
                else:
                    org_type = st.text_input("Organization Type")
                    org_name = st.text_input("Organization Name")

        elif donor_status == "Existing Donor":
            donor_ids = ["None"] + [row[0] for row in run_query("SELECT DONOR_ID FROM donor")]
            donor_id = st.selectbox("Select Donor ID", donor_ids)

        with st.form("donation_form"):
            # Donation Date
            donation_date = st.date_input("Donation Date")

            # Goods Type
            goods_types = ["None"] + [row[0] for row in run_query("SELECT PRODTYPE_NAME FROM product_types")]
            goods_type = st.selectbox("Goods Type", goods_types)

            # Goods Condition
            goods_conditions = ["None"] + [row[0] for row in run_query("SELECT DISTINCT PRICING_CONDITION FROM products")]
            goods_condition = st.selectbox("Goods Condition", goods_conditions)

            # Event Name
            event_names = ["None"] + [row[0] for row in run_query("SELECT EVENT_NAME FROM events")]
            event_name = st.selectbox("Event Name", event_names)

            event_id = None
            if event_name != "None":
                event_id = run_query(
                    "SELECT EVENT_ID FROM events WHERE EVENT_NAME = :event_name",
                    {"event_name": event_name}
                )[0][0]

            # Select Center ID
            center_choices = {
                "None": None,
                "Phoenix Donation Center": 1,
                "Tucson Relief Hub": 2,
                "Flagstaff Giving Center": 3,
                "Mesa Charity Center": 4,
                "Chandler Assistance Hub": 5
            }
            center_name = st.selectbox("Center Name", list(center_choices.keys()))
            center_id = center_choices[center_name]

            # Donation Quantity
            donation_qty = st.number_input("Donation Quantity", min_value=1, step=1)

            submitted = st.form_submit_button("Submit")

            if submitted:
                try:
                    # Determine the donor_id based on donor status (new or existing)
                    if donor_status == "New Donor":
                        # Insert into donor table
                        run_query("""
                            INSERT INTO donor (email_id, phone, street, state, zip, donor_type)
                            VALUES (:email, :phone, :street, :state, :zip, :donor_type)
                        """, {
                            "email": email,
                            "phone": phone,
                            "street": street,
                            "state": state,
                            "zip": zip_code,
                            "donor_type": donor_type
                        })

                        # Fetch the most recently added donor_id using Oracle-specific syntax
                        new_donor_id = run_query("""
                            SELECT donor_id FROM donor ORDER BY donor_id DESC FETCH FIRST 1 ROWS ONLY
                        """)[0][0]

                        # Insert into individual_donor or organization_donor based on donor type
                        if donor_type == "INDV":
                            run_query("""
                                INSERT INTO individual_donor (donor_id, d_first_name, d_last_name, age, gender)
                                VALUES (:donor_id, :first_name, :last_name, :age, :gender)
                            """, {
                                "donor_id": new_donor_id,
                                "first_name": first_name,
                                "last_name": last_name,
                                "age": age,
                                "gender": gender
                            })
                        else:
                            run_query("""
                                INSERT INTO organization_donor (donor_id, org_type, d_name)
                                VALUES (:donor_id, :org_type, :org_name)
                            """, {
                                "donor_id": new_donor_id,
                                "org_type": org_type,
                                "org_name": org_name
                            })

                        donor_id = new_donor_id  # Assign the new donor id to the general donor_id variable

                    elif donor_status == "Existing Donor":
                        donor_id = donor_id  # For existing donor, use the selected donor_id

                    # Handle Donations
                    run_query("""
                        INSERT INTO donations 
                        (donation_date, goods_type, goods_condition, event_id, donor_id, center_id, donation_qty)
                        VALUES (:donation_date, :goods_type, :goods_condition, :event_id, :donor_id, :center_id, :donation_qty)
                    """, {
                        "donation_date": donation_date,
                        "goods_type": goods_type if goods_type != "None" else None,
                        "goods_condition": goods_condition if goods_condition != "None" else None,
                        "event_id": event_id,
                        "donor_id": donor_id,  # Use the correct donor_id here (either new or existing)
                        "center_id": center_id,
                        "donation_qty": donation_qty
                    })

                    st.success("Donation added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif action == "View":
        try:
            results = run_query("SELECT * FROM donations")
            if results:
                df = pd.DataFrame(results, columns=["ID", "Donation Date", "Goods Type", "Goods Condition", "Donor ID", "Center ID", "Product ID", "Event ID", "Donation Quantity"])
                st.dataframe(df)
            else:
                st.write("No donations found.")
        except Exception as e:
            st.error(f"Error fetching donations: {e}")

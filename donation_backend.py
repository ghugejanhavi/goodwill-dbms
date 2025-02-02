from asyncio.windows_events import NULL
import streamlit as st
import pandas as pd
from utils import run_query, render_goodwill_header

def donations_page():
    # Create columns, the first for the header and the second for the "Back to Home" button
    col1, col2 = st.columns([5, 1])  # First column takes more space for the header, second column for button

    with col1:
        # Render the company header (logo and title)
        render_goodwill_header()

    with col2:
        # Place the "Back to Home" button in the right column
        if st.button("Back"):
            st.session_state.page = "home"
            st.experimental_rerun()

    st.header("Donations Management")

    action = st.selectbox("Action", ["Create", "View"])

    if action == "Create":
        with st.form("donation_form"):
            # Donation Date
            donation_date = st.date_input("Donation Date")

            # Fetch available goods types from product_type table with a default value of None
            goods_types = ["None"] + [row[0] for row in run_query("SELECT PRODTYPE_NAME FROM product_types")]
            goods_type = st.selectbox("Goods Type", goods_types)

            # Fetch available product conditions from pricing table with a default value of None
            goods_conditions = ["None"] + [row[0] for row in run_query("SELECT DISTINCT PRICING_CONDITION FROM products")]
            goods_condition = st.selectbox("Goods Condition", goods_conditions)

            # Fetch event names from events table
            event_names = ["None"] + [row[0] for row in run_query("SELECT EVENT_NAME FROM events")]
            event_name = st.selectbox("Event Name", event_names)
            

            # Fetch corresponding Event ID for the selected event name
            event_id = NULL
            # if event_name != "None":
            #     event_id_row = run_query(
            #         "SELECT EVENT_ID FROM events WHERE EVENT_NAME = :event_name",
            #         {"event_name": event_name}
            #     ).fetchone()
            #     if event_id_row:
            #         event_id = event_id_row[0]

            # Fetch donor IDs from the donor table with a default value of None
            donor_ids = ["None"] + [row[0] for row in run_query("SELECT DONOR_ID FROM donor")]
            donor_id = st.selectbox("Donor ID", donor_ids)

            # Select Center ID from hardcoded values
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
            # Submit button
            submitted = st.form_submit_button("Submit")

            if submitted:
                if event_id and donor_id != "None" and center_id:
                    try:
                        run_query("""
                            INSERT INTO donations 
                            (donation_date, goods_type, goods_condition, event_id, donor_id, center_id, donation_qty)
                            VALUES (:donation_date, :goods_type, :goods_condition, :event_id, :donor_id, :center_id, :donation_qty)
                        """, {
                            "donation_date": donation_date,
                            "goods_type": goods_type if goods_type != "None" else None,
                            "goods_condition": goods_condition if goods_condition != "None" else None,
                            "event_id": event_id,
                            "donor_id": donor_id,
                            "center_id": center_id,
                            "donation_qty": donation_qty
                        })
                        st.success("Donation added successfully!")
                    except Exception as e:
                        st.error(f"Error inserting donation: {e}")
                else:
                    st.error("Please select valid values for all fields.")

    elif action == "View":
        # View donations
        try:
            results = run_query("SELECT * FROM donations")
            if results:
                df = pd.DataFrame(results, columns=["ID", "Donation Date", "Goods Type", "Goods Condition", "Event ID", "Donor ID", "Center ID", "Product ID", "Donation Quantity"])
                st.dataframe(df)
            else:
                st.write("No donations found.")
        except Exception as e:
            st.error(f"Error fetching donations: {e}")

# Call this function in your main app file where routing occurs

import streamlit as st
import pandas as pd
from utils import run_query, render_goodwill_header

def events_page():
    # Initialize session state flags if they don't exist
    if "submit_event_button" not in st.session_state:
        st.session_state.submit_event_button = False
    if "update_event_button_clicked" not in st.session_state:
        st.session_state.update_event_button_clicked = False

    # Header and navigation
    col1, col2 = st.columns([5, 1])
    
    with col1:
        render_goodwill_header()
    
    with col2:
        if st.button("Back"):
            st.session_state.page = "home"
            st.experimental_rerun()

    st.header("Events Management")
    action = st.selectbox("Action", ["Create", "View"])

    if action == "Create":
        with st.form("event_form"):
            event_date = st.date_input("Event Date")
            event_name = st.text_input("Event Name")
            event_street = st.text_input("Street Address")
            event_state = st.text_input("State")
            event_zip = st.text_input("ZIP Code")

            # Fetch available teams for the selected date
            teams = run_query("""
                SELECT event_team_id, event_team_name 
                FROM event_teams 
                WHERE event_team_id NOT IN (
                    SELECT event_team_id 
                    FROM events 
                    WHERE event_date = :event_date
                )
            """, {"event_date": event_date})
            
            if teams:
                team_dict = {f"{team[1]} (ID: {team[0]})": team[0] for team in teams}
                selected_team = st.selectbox("Event Team", list(team_dict.keys()))
            else:
                st.warning("No available teams for the selected date.")
                selected_team = None

            # Dropdown for store name
            stores = run_query("SELECT store_id, s_store_name FROM retail_stores")
            store_dict = {f"{store[1]} (ID: {store[0]})": store[0] for store in stores}
            selected_store = st.selectbox("Store Name", list(store_dict.keys()))

            submitted = st.form_submit_button("Submit", on_click=callback)
            
            if submitted:
                try:
                    run_query(
                        """
                        INSERT INTO events (
                            event_date, event_name, event_street, event_state, event_zip, event_team_id, store_id
                        )
                        VALUES (
                            :event_date, :event_name, :event_street, :event_state, :event_zip, :event_team_id, :store_id
                        )
                        """,
                        {
                            "event_date": event_date,
                            "event_name": event_name,
                            "event_street": event_street,
                            "event_state": event_state,
                            "event_zip": event_zip,
                            "event_team_id": team_dict[selected_team],
                            "store_id": store_dict[selected_store],
                        }
                    )
                    st.success("Event added successfully!")
                except Exception as e:
                    st.error(f"Error adding event: {e}")

    elif action == "View":
        def display_event_table():
            try:
                results = run_query(
                    """
                    SELECT e.event_id, e.event_date, e.event_name, e.event_street, e.event_state, e.event_zip,
                        t.event_team_name, s.s_store_name
                    FROM events e
                    JOIN event_teams t ON e.event_team_id = t.event_team_id
                    JOIN retail_stores s ON e.store_id = s.store_id
                    """
                )
                if results:
                    df = pd.DataFrame(results, columns=[
                        "Event ID", "Event Date", "Event Name", "Street Address",
                        "State", "ZIP Code", "Event Team Name", "Store Name"
                    ])
                    st.dataframe(df)
                    return df
                else:
                    st.write("No events found.")
                    return None
            except Exception as e:
                st.error(f"Error fetching events: {e}")
                return None

        df = display_event_table()

        if df is not None and not df.empty:
            # Delete event
            event_to_delete = st.text_input("Enter Event ID to Delete")
            if st.button("Delete") and event_to_delete:
                try:
                    run_query("DELETE FROM events WHERE event_id = :event_id", {"event_id": event_to_delete})
                    st.success("Event deleted successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error deleting event: {e}")

            # Update event
            event_to_update = st.text_input("Enter Event ID to Update")
            if event_to_update:
                event_row = run_query(
                    """
                    SELECT e.*, t.event_team_name, s.s_store_name
                    FROM events e
                    JOIN event_teams t ON e.event_team_id = t.event_team_id
                    JOIN retail_stores s ON e.store_id = s.store_id
                    WHERE e.event_id = :event_id
                    """,
                    {"event_id": event_to_update}
                )

                if event_row:
                    event_data = event_row[0]
                    event_data_new = list(event_data)
                    event_data_new.pop()
                    event_data_new.pop()
                    event_data = tuple(event_data_new)
                    if len(event_data) == 8:  # Adjust based on actual columns returned
                        with st.form("update_event_form"):
                            updated_date = st.date_input("Event Date", value=pd.to_datetime(event_data[1]))
                            updated_name = st.text_input("Event Name", value=event_data[2])
                            updated_street = st.text_input("Street Address", value=event_data[3])
                            updated_state = st.text_input("State", value=event_data[4])
                            updated_zip = st.text_input("ZIP Code", value=event_data[5])

                            # Fetch teams and stores for dropdowns (re-initialize inside form)
                            teams = run_query("SELECT event_team_id, event_team_name FROM event_teams")
                            team_dict = {f"{team[1]} (ID: {team[0]})": team[0] for team in teams}

                            stores = run_query("SELECT store_id, s_store_name FROM retail_stores")
                            store_dict = {f"{store[1]} (ID: {store[0]})": store[0] for store in stores}

                            # Preselect event team
                            selected_team = st.selectbox(
                                "Event Team",
                                list(team_dict.keys()),
                                index=list(team_dict.values()).index(event_data[6])  # Using event_team_id for pre-selection
                            )

                            # Preselect store name
                            selected_store = st.selectbox(
                                "Store Name",
                                list(store_dict.keys()),
                                index=list(store_dict.values()).index(event_data[7])  # Using store_id for pre-selection
                            )

                            update_submitted = st.form_submit_button("Save Update", on_click=callback_2)

                            if update_submitted:
                                try:
                                    run_query(
                                        """
                                        UPDATE events 
                                        SET event_date = :event_date, event_name = :event_name, 
                                            event_street = :event_street, event_state = :event_state, 
                                            event_zip = :event_zip, event_team_id = :event_team_id, 
                                            store_id = :store_id
                                        WHERE event_id = :event_id
                                        """,
                                        {
                                            "event_id": event_to_update,
                                            "event_date": updated_date,
                                            "event_name": updated_name,
                                            "event_street": updated_street,
                                            "event_state": updated_state,
                                            "event_zip": updated_zip,
                                            "event_team_id": team_dict[selected_team],
                                            "store_id": store_dict[selected_store],
                                        }
                                    )
                                    st.success("Event updated successfully!")
                                    st.experimental_rerun()
                                except Exception as e:
                                    st.error(f"Error updating event: {e}")
                    else:
                        st.error("Event data is not in the expected format.")
                else:
                    st.error("Event ID not found.")


# Callback functions
def callback():
    st.session_state.submit_event_button = True

def callback_2():
    st.session_state.update_event_button_clicked = True
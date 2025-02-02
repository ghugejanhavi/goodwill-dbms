import streamlit as st
import plotly.express as px
import pandas as pd
from utils import run_query, render_goodwill_header

def analytics_page():
    # Create columns for the header and "Back" button
    col1, col2 = st.columns([5, 1])

    with col1:
        render_goodwill_header()

    with col2:
        if st.button("Back"):
            st.session_state.page = "home"
            st.experimental_rerun()

    st.title("Reports and Analytics")

    # New Chart: Total Revenue by Store and Product Type
    st.subheader("1. Total Revenue by Store and Product Type")
    revenue_data = run_query("""
        SELECT 
            r.s_store_name,
            p1.prodtype_name AS Product_Name,
            to_char(SUM(od.qty * p.net_unit_price), '$999999.99') AS total_revenue
        FROM RETAIL_STORES r 
        LEFT JOIN INSTORE_ORDERS io ON r.store_id = io.store_id
        LEFT JOIN INSTORE_ORDER_DETAILS od ON od.instore_order_id = io.instore_order_id
        LEFT JOIN PRODUCTS p ON p.product_id = od.product_id
        LEFT JOIN PRODUCT_TYPES p1 ON p1.prodtypeID = p.prodtypeID
        GROUP BY CUBE(p1.prodtype_name, r.s_store_name)
        ORDER BY total_revenue DESC
    """)
    revenue_df = pd.DataFrame(revenue_data, columns=["Store Name", "Product Type", "Total Revenue"])
    fig1 = px.bar(revenue_df, x="Store Name", y="Total Revenue", color="Product Type", title="Total Revenue by Store and Product Type")
    st.plotly_chart(fig1)

    st.subheader("2. Donations by Goods Type")
    goods_data = run_query("SELECT goods_type, SUM(donation_qty) FROM donations GROUP BY goods_type ORDER BY SUM(donation_qty) DESC")
    goods_df = pd.DataFrame(goods_data, columns=["Goods Type", "Count"])
    fig2 = px.bar(goods_df, x="Goods Type", y="Count", title="Donations by Goods Type")
    st.plotly_chart(fig2)

    st.subheader("3. Donations by Center")
    center_data = run_query("""
        SELECT dc.dc_name AS Center_Name, COUNT(d.donation_id) AS Count
        FROM donations d
        JOIN donation_center dc ON d.center_id = dc.center_id
        GROUP BY dc.dc_name
        ORDER BY Count DESC
    """)
    center_df = pd.DataFrame(center_data, columns=["Center Name", "Count"])
    fig3 = px.pie(center_df, names="Center Name", values="Count", title="Donations by Center")
    st.plotly_chart(fig3)

    st.subheader("4. Donation Source Breakdown")

    # Query for individual donations
    individual_data = run_query("""
        SELECT SUM(donation_qty) 
        FROM DONATIONS do
        INNER JOIN DONOR don ON do.donor_id = don.donor_id
        WHERE don.donor_type = 'INDV' AND do.event_id IS NULL
    """)

    # Query for organization donations
    organization_data = run_query("""
        SELECT SUM(donation_qty) 
        FROM DONATIONS do
        INNER JOIN DONOR don ON do.donor_id = don.donor_id
        WHERE don.donor_type = 'ORG' AND do.event_id IS NULL
    """)

    # Query for event donations
    event_data = run_query("""
        SELECT SUM(donation_qty) 
        FROM DONATIONS do
        INNER JOIN DONOR don ON do.donor_id = don.donor_id
        WHERE do.event_id IS NOT NULL
    """)

    # Check if all donation types returned data
    if individual_data and organization_data and event_data:
        total_donations = individual_data[0][0] + organization_data[0][0] + event_data[0][0]

        if total_donations > 0:
            # Calculate percentages
            individual_percentage = (individual_data[0][0] / total_donations) * 100
            organization_percentage = (organization_data[0][0] / total_donations) * 100
            event_percentage = (event_data[0][0] / total_donations) * 100

            # Prepare data for pie chart
            pie_data = pd.DataFrame({
                "Donation Type": ["Individual Donations", "Organization Donations", "Event Donations"],
                "Percentage": [individual_percentage, organization_percentage, event_percentage]
            })

            # Plot the pie chart using Plotly
            fig4 = px.pie(pie_data, names="Donation Type", values="Percentage", title="Donation Source Breakdown")
            st.plotly_chart(fig4)
        else:
            st.warning("Total donations are zero.")
    else:
        st.warning("No donation data available for the source breakdown.")
    
    # 5th Chart: Top 5 Donors by Quantity Donated
    st.subheader("5. Top 5 Donors by Quantity Donated")
    
    # Query to fetch the top 5 donors based on donation quantity
    top_donors_data = run_query("""
        SELECT d.donor_ID, d_first_name || ' ' || d_last_name AS Top_Donors, SUM(donation_qty) AS Qty_Donated 
        FROM donations d 
        JOIN individual_donor d1 ON d.donor_id = d1.donor_id
        GROUP BY d.donor_ID, d_first_name, d_last_name
        ORDER BY Qty_Donated DESC
        FETCH FIRST 5 ROWS ONLY
    """)

    if top_donors_data:
        # Create a DataFrame for the top donors data
        top_donors_df = pd.DataFrame(top_donors_data, columns=["Donor ID", "Top Donors", "Qty Donated"])

        # Create a bar chart to display top 5 donors
        fig5 = px.bar(top_donors_df, x="Top Donors", y="Qty Donated", title="Top 5 Donors by Quantity Donated")
        st.plotly_chart(fig5)
    else:
        st.warning("No data available for the top donors.")

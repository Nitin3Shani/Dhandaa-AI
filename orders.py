"""
Orders management module
Handles all order-related operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_manager import get_user_data, save_user_data
from config import ORDER_STATUSES

def show_orders_page(username):
    """Display orders management page"""
    st.title("📋 Orders Management")
    
    tab1, tab2 = st.tabs(["Add Order", "View Orders"])
    
    with tab1:
        add_order_form(username)
    
    with tab2:
        view_orders_table(username)

def add_order_form(username):
    """Form to add a new order"""
    st.subheader("Record New Order")
    
    with st.form("add_order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            order_name = st.text_input("Order Description*")
            amount = st.number_input("Order Amount (₹)*", min_value=0.0, value=0.0, step=0.01, format="%.2f")
            customer = st.text_input("Customer Name*")
        
        with col2:
            status = st.selectbox("Status*", ORDER_STATUSES)
            order_date = st.date_input("Order Date*", value=datetime.now())
            due_date = st.date_input("Due Date*", value=datetime.now() + timedelta(days=7))
        
        notes = st.text_area("Notes (Optional)")
        
        submitted = st.form_submit_button("Add Order", type="primary", use_container_width=True)
        
        if submitted:
            if order_name and amount > 0 and customer:
                order_data = {
                    'id': len(get_user_data(username, 'orders')) + 1,
                    'description': order_name,
                    'amount': amount,
                    'customer': customer,
                    'status': status,
                    'order_date': str(order_date),
                    'due_date': str(due_date),
                    'notes': notes if notes else ""
                }
                
                save_user_data(username, 'orders', order_data)
                st.success("✅ Order added successfully!")
                st.rerun()
            else:
                st.error("Please fill all required fields")

def view_orders_table(username):
    """Display orders records in a table"""
    orders = get_user_data(username, 'orders')
    
    if orders:
        df = pd.DataFrame(orders)
        
        # Convert dates
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['due_date'] = pd.to_datetime(df['due_date'])
        
        # Calculate days until due
        df['days_to_due'] = (df['due_date'] - datetime.now()).dt.days
        
        # Format amounts
        df['amount_fmt'] = df['amount'].apply(lambda x: f"₹{x:,.2f}")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=ORDER_STATUSES,
                default=["Pending", "Completed"]
            )
        
        with col2:
            sort_by = st.selectbox("Sort by", ["Due Date", "Amount", "Order Date"])
        
        # Apply status filter
        filtered_df = df[df['status'].isin(status_filter)]
        
        # Apply sorting
        if sort_by == "Due Date":
            filtered_df = filtered_df.sort_values('due_date')
        elif sort_by == "Amount":
            filtered_df = filtered_df.sort_values('amount', ascending=False)
        else:
            filtered_df = filtered_df.sort_values('order_date', ascending=False)
        
        # Display columns
        display_df = filtered_df[['id', 'description', 'customer', 'amount_fmt', 'status', 'order_date', 'due_date', 'days_to_due']]
        display_df.columns = ['ID', 'Description', 'Customer', 'Amount', 'Status', 'Order Date', 'Due Date', 'Days to Due']
        
        # Styling based on status and due date
        def highlight_orders(row):
            if row['Status'] == 'Pending' and row['Days to Due'] < 0:
                return ['background-color: #ffcccc'] * len(row)  # Overdue
            elif row['Status'] == 'Pending' and row['Days to Due'] <= 3:
                return ['background-color: #fff4cc'] * len(row)  # Due soon
            elif row['Status'] == 'Completed':
                return ['background-color: #ccffcc'] * len(row)  # Completed
            return [''] * len(row)
        
        st.dataframe(
            display_df.style.apply(highlight_orders, axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        st.caption("🔴 Overdue | 🟡 Due Soon | 🟢 Completed")
        
        # Summary statistics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_orders = len(orders)
            st.metric("Total Orders", total_orders)
        
        with col2:
            pending_count = len([o for o in orders if o['status'] == 'Pending'])
            st.metric("Pending Orders", pending_count)
        
        with col3:
            pending_value = sum(o['amount'] for o in orders if o['status'] == 'Pending')
            st.metric("Pending Value", f"₹{pending_value:,.2f}")
        
        with col4:
            completed_value = sum(o['amount'] for o in orders if o['status'] == 'Completed')
            st.metric("Completed Value", f"₹{completed_value:,.2f}")
        
        # Download option
        st.markdown("---")
        csv = pd.DataFrame(orders).to_csv(index=False)
        st.download_button(
            label="📥 Download Orders Data (CSV)",
            data=csv,
            file_name=f"orders_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No orders recorded yet. Add your first order above!")

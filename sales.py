"""
Sales management module
Handles all sales-related operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from data_manager import get_user_data, save_user_data

def show_sales_page(username):
    """Display sales management page"""
    st.title("💰 Sales Management")
    
    tab1, tab2 = st.tabs(["Add Sale", "View Sales"])
    
    with tab1:
        add_sale_form(username)
    
    with tab2:
        view_sales_table(username)

def add_sale_form(username):
    """Form to add a new sale"""
    st.subheader("Record New Sale")
    
    with st.form("add_sale_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product = st.text_input("Product Name*")
            quantity = st.number_input("Quantity*", min_value=1, value=1)
            unit_price = st.number_input("Unit Price (₹)*", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        
        with col2:
            cost_per_unit = st.number_input("Cost per Unit (₹)*", min_value=0.0, value=0.0, step=0.01, format="%.2f")
            sale_date = st.date_input("Sale Date*", value=datetime.now())
            customer_name = st.text_input("Customer Name (Optional)")
        
        # Calculate totals
        total_amount = quantity * unit_price
        total_cost = quantity * cost_per_unit
        profit = total_amount - total_cost
        
        st.markdown(f"""
        **Summary:**
        - Total Amount: ₹{total_amount:.2f}
        - Total Cost: ₹{total_cost:.2f}
        - **Profit: ₹{profit:.2f}**
        """)
        
        submitted = st.form_submit_button("Add Sale", type="primary", use_container_width=True)
        
        if submitted:
            if product and unit_price > 0:
                sale_data = {
                    'id': len(get_user_data(username, 'sales')) + 1,
                    'product': product,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_amount': total_amount,
                    'cost': total_cost,
                    'profit': profit,
                    'customer': customer_name if customer_name else "N/A",
                    'date': str(sale_date)
                }
                
                save_user_data(username, 'sales', sale_data)
                st.success("✅ Sale recorded successfully!")
                st.rerun()
            else:
                st.error("Please fill all required fields")

def view_sales_table(username):
    """Display sales records in a table"""
    sales = get_user_data(username, 'sales')
    
    if sales:
        df = pd.DataFrame(sales)
        
        # Format currency columns
        df['unit_price'] = df['unit_price'].apply(lambda x: f"₹{x:.2f}")
        df['total_amount'] = df['total_amount'].apply(lambda x: f"₹{x:.2f}")
        df['profit'] = df['profit'].apply(lambda x: f"₹{x:.2f}")
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        sales_raw = get_user_data(username, 'sales')
        
        with col1:
            total_sales = sum(s['total_amount'] for s in sales_raw)
            st.metric("Total Sales", f"₹{total_sales:,.2f}")
        
        with col2:
            total_profit = sum(s['profit'] for s in sales_raw)
            st.metric("Total Profit", f"₹{total_profit:,.2f}")
        
        with col3:
            st.metric("Number of Sales", len(sales_raw))
        
        # Download option
        st.markdown("---")
        csv = pd.DataFrame(sales_raw).to_csv(index=False)
        st.download_button(
            label="📥 Download Sales Data (CSV)",
            data=csv,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No sales recorded yet. Add your first sale above!")

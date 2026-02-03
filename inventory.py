"""
Inventory management module
Handles all inventory-related operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from data_manager import get_user_data, save_user_data
from config import INVENTORY_CATEGORIES

def show_inventory_page(username):
    """Display inventory management page"""
    st.title("📦 Inventory Management")
    
    tab1, tab2 = st.tabs(["Add Item", "View Inventory"])
    
    with tab1:
        add_inventory_form(username)
    
    with tab2:
        view_inventory_table(username)

def add_inventory_form(username):
    """Form to add a new inventory item"""
    st.subheader("Add Inventory Item")
    
    with st.form("add_inventory_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            item_name = st.text_input("Item Name*")
            quantity = st.number_input("Quantity*", min_value=0, value=0)
            unit_price = st.number_input("Unit Price (₹)*", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        
        with col2:
            category = st.selectbox("Category*", INVENTORY_CATEGORIES)
            reorder_level = st.number_input("Reorder Level", min_value=0, value=10, 
                                           help="Alert when stock falls below this level")
            supplier = st.text_input("Supplier (Optional)")
        
        notes = st.text_area("Notes (Optional)")
        
        total_value = quantity * unit_price
        st.info(f"**Total Inventory Value:** ₹{total_value:,.2f}")
        
        submitted = st.form_submit_button("Add Item", type="primary", use_container_width=True)
        
        if submitted:
            if item_name and quantity >= 0:
                inventory_data = {
                    'id': len(get_user_data(username, 'inventory')) + 1,
                    'name': item_name,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'category': category,
                    'reorder_level': reorder_level,
                    'supplier': supplier if supplier else "N/A",
                    'notes': notes if notes else "",
                    'added_date': str(datetime.now().date())
                }
                
                save_user_data(username, 'inventory', inventory_data)
                st.success("✅ Item added to inventory!")
                st.rerun()
            else:
                st.error("Please fill all required fields")

def view_inventory_table(username):
    """Display inventory records in a table"""
    inventory = get_user_data(username, 'inventory')
    
    if inventory:
        df = pd.DataFrame(inventory)
        
        # Calculate inventory value
        df['total_value'] = df['quantity'] * df['unit_price']
        
        # Check stock status
        df['status'] = df.apply(lambda row: 
            '🔴 Low Stock' if row['quantity'] < row['reorder_level'] 
            else '🟢 In Stock', axis=1)
        
        # Format currency columns
        df['unit_price_fmt'] = df['unit_price'].apply(lambda x: f"₹{x:.2f}")
        df['total_value_fmt'] = df['total_value'].apply(lambda x: f"₹{x:.2f}")
        
        # Display columns
        display_df = df[['name', 'category', 'quantity', 'unit_price_fmt', 'total_value_fmt', 'reorder_level', 'status', 'supplier']]
        display_df.columns = ['Item', 'Category', 'Qty', 'Unit Price', 'Total Value', 'Reorder Level', 'Status', 'Supplier']
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.multiselect(
                "Filter by Category",
                options=df['category'].unique(),
                default=df['category'].unique()
            )
        with col2:
            status_filter = st.multiselect(
                "Filter by Status",
                options=['🟢 In Stock', '🔴 Low Stock'],
                default=['🟢 In Stock', '🔴 Low Stock']
            )
        
        # Apply filters
        filtered_df = display_df[
            (df['category'].isin(category_filter)) & 
            (df['status'].isin(status_filter))
        ]
        
        # Apply styling
        def highlight_low_stock(row):
            if row['Status'] == '🔴 Low Stock':
                return ['background-color: #ffcccc'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            filtered_df.style.apply(highlight_low_stock, axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        # Summary statistics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_items = len(inventory)
            st.metric("Total Items", total_items)
        
        with col2:
            total_value = sum(item['quantity'] * item['unit_price'] for item in inventory)
            st.metric("Total Value", f"₹{total_value:,.2f}")
        
        with col3:
            low_stock_count = len([item for item in inventory if item['quantity'] < item['reorder_level']])
            st.metric("Low Stock Items", low_stock_count, delta="Action Needed" if low_stock_count > 0 else None)
        
        with col4:
            out_of_stock = len([item for item in inventory if item['quantity'] == 0])
            st.metric("Out of Stock", out_of_stock)
        
        # Download option
        st.markdown("---")
        csv = pd.DataFrame(inventory).to_csv(index=False)
        st.download_button(
            label="📥 Download Inventory Data (CSV)",
            data=csv,
            file_name=f"inventory_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No inventory items yet. Add your first item above!")

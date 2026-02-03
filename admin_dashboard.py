"""
Admin dashboard module
Admin panel for viewing and managing all businesses
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from data_manager import load_json
from config import USERS_FILE, BUSINESSES_FILE, SALES_FILE

def show_admin_dashboard():
    """Display admin dashboard"""
    st.title("🔐 Admin Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.title("👨‍💼 Admin Panel")
        st.markdown("---")
        
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    # Load data
    users = load_json(USERS_FILE)
    businesses = load_json(BUSINESSES_FILE)
    
    # Filter out admin
    user_list = {k: v for k, v in users.items() if v['type'] == 'user'}
    
    # Platform overview
    display_platform_overview(user_list)
    
    st.markdown("---")
    
    # Business list
    display_business_list(user_list)
    
    st.markdown("---")
    
    # Analytics
    display_platform_analytics(user_list)

def display_platform_overview(user_list):
    """Display platform-wide metrics"""
    st.subheader("📊 Platform Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Businesses", len(user_list))
    
    with col2:
        total_sales_count = sum(
            len(load_json(SALES_FILE).get(u, [])) 
            for u in user_list.keys()
        )
        st.metric("Total Sales Records", total_sales_count)
    
    with col3:
        active_today = len([
            u for u in user_list.values() 
            if (datetime.now() - datetime.fromisoformat(u['created_at'])).days < 1
        ])
        st.metric("Registered Today", active_today)
    
    with col4:
        active_week = len([
            u for u in user_list.values() 
            if (datetime.now() - datetime.fromisoformat(u['created_at'])).days < 7
        ])
        st.metric("Active This Week", active_week)

def display_business_list(user_list):
    """Display list of registered businesses"""
    st.subheader("📋 Registered Businesses")
    
    if user_list:
        business_data = []
        sales_data = load_json(SALES_FILE)
        
        for username, user_info in user_list.items():
            sales_count = len(sales_data.get(username, []))
            user_sales = sales_data.get(username, [])
            total_revenue = sum(sale['total_amount'] for sale in user_sales)
            
            business_data.append({
                'Username': username,
                'Business Name': user_info.get('business_name', 'N/A'),
                'Type': user_info.get('business_type', 'N/A'),
                'Sales Records': sales_count,
                'Revenue': f"₹{total_revenue:,.2f}",
                'Registered': user_info['created_at'][:10]
            })
        
        df = pd.DataFrame(business_data)
        
        # Search and filter
        col1, col2 = st.columns([2, 1])
        
        with col1:
            search = st.text_input("🔍 Search by username or business name", "")
        
        with col2:
            business_type_filter = st.multiselect(
                "Filter by Type",
                options=df['Type'].unique(),
                default=df['Type'].unique()
            )
        
        # Apply filters
        if search:
            df = df[
                df['Username'].str.contains(search, case=False) | 
                df['Business Name'].str.contains(search, case=False)
            ]
        
        df = df[df['Type'].isin(business_type_filter)]
        
        # Display table
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Business List (CSV)",
            data=csv,
            file_name=f"businesses_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No businesses registered yet")

def display_platform_analytics(user_list):
    """Display platform-wide analytics"""
    st.subheader("📊 Platform Analytics")
    
    if not user_list:
        st.info("No data available yet")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Business type distribution
        business_types = [user.get('business_type', 'Other') for user in user_list.values()]
        type_counts = pd.Series(business_types).value_counts()
        
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title='Businesses by Type'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Registration timeline
        registration_dates = [
            datetime.fromisoformat(user['created_at']).date() 
            for user in user_list.values()
        ]
        reg_df = pd.DataFrame({'date': registration_dates})
        reg_counts = reg_df.groupby('date').size().reset_index(name='count')
        
        fig = px.bar(
            reg_counts,
            x='date',
            y='count',
            title='Daily Registrations',
            labels={'date': 'Date', 'count': 'New Businesses'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sales activity across platform
    sales_data = load_json(SALES_FILE)
    
    if sales_data:
        st.markdown("#### Platform-wide Sales Activity")
        
        all_sales = []
        for username, sales_list in sales_data.items():
            if username in user_list:
                for sale in sales_list:
                    all_sales.append({
                        'business': user_list[username].get('business_name', username),
                        'amount': sale['total_amount'],
                        'date': sale['date']
                    })
        
        if all_sales:
            sales_df = pd.DataFrame(all_sales)
            sales_df['date'] = pd.to_datetime(sales_df['date'])
            
            # Daily platform revenue
            daily_revenue = sales_df.groupby(sales_df['date'].dt.date)['amount'].sum().reset_index()
            daily_revenue.columns = ['Date', 'Revenue']
            
            fig = px.area(
                daily_revenue,
                x='Date',
                y='Revenue',
                title='Platform Daily Revenue',
                labels={'Revenue': 'Total Revenue (₹)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Top performing businesses
            top_businesses = sales_df.groupby('business')['amount'].sum().sort_values(ascending=False).head(10)
            
            fig = px.bar(
                x=top_businesses.values,
                y=top_businesses.index,
                orientation='h',
                title='Top 10 Businesses by Revenue',
                labels={'x': 'Revenue (₹)', 'y': 'Business'}
            )
            st.plotly_chart(fig, use_container_width=True)

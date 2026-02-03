"""
User dashboard module
Orchestrates all user-facing pages and navigation
"""

import streamlit as st
from dashboard import show_dashboard_page
from sales import show_sales_page
from inventory import show_inventory_page
from orders import show_orders_page
from debts import show_debts_page
from analytics_page import show_analytics_page

def show_user_dashboard():
    """Display user dashboard with navigation"""
    username = st.session_state.username
    
    # Sidebar navigation
    with st.sidebar:
        st.title(f"👤 {st.session_state.business_name}")
        st.caption(f"@{username}")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "💰 Sales",
                "📦 Inventory",
                "📋 Orders",
                "💳 Debts",
                "📈 Analytics"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.session_state.business_name = None
            st.rerun()
        
        # Quick stats in sidebar
        display_sidebar_stats(username)
    
    # Main content area - route to appropriate page
    if page == "📊 Dashboard":
        show_dashboard_page(username)
    elif page == "💰 Sales":
        show_sales_page(username)
    elif page == "📦 Inventory":
        show_inventory_page(username)
    elif page == "📋 Orders":
        show_orders_page(username)
    elif page == "💳 Debts":
        show_debts_page(username)
    elif page == "📈 Analytics":
        show_analytics_page(username)

def display_sidebar_stats(username):
    """Display quick stats in sidebar"""
    from analytics import calculate_metrics
    
    metrics = calculate_metrics(username)
    
    if metrics:
        st.markdown("### 📊 Quick Stats")
        st.metric("Revenue", f"₹{metrics['total_revenue']:,.0f}", label_visibility="visible")
        st.metric("Profit", f"₹{metrics['total_profit']:,.0f}", label_visibility="visible")
        st.metric("Margin", f"{metrics['profit_margin']:.1f}%", label_visibility="visible")
    else:
        st.info("Start recording sales to see stats!")

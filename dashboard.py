"""
Dashboard module
Main dashboard with key metrics and AI insights
"""

import streamlit as st
import plotly.express as px
from analytics import calculate_metrics, generate_insights

def show_dashboard_page(username):
    """Display main dashboard with metrics and insights"""
    st.title("📊 Business Dashboard")
    
    metrics = calculate_metrics(username)
    
    if metrics:
        # Key Performance Indicators
        display_kpi_metrics(metrics)
        
        st.markdown("---")
        
        # AI-Powered Insights
        display_ai_insights(username)
        
        st.markdown("---")
        
        # Quick Overview Charts
        display_quick_charts(metrics)
    else:
        display_welcome_message()

def display_kpi_metrics(metrics):
    """Display key performance indicator metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"₹{metrics['total_revenue']:,.2f}")
    
    with col2:
        st.metric("Total Profit", f"₹{metrics['total_profit']:,.2f}")
    
    with col3:
        st.metric("Profit Margin", f"{metrics['profit_margin']:.1f}%")
    
    with col4:
        st.metric("Inventory Value", f"₹{metrics['inventory_value']:,.2f}")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Pending Orders", f"₹{metrics['pending_orders']:,.2f}")
    
    with col6:
        delta_text = "Collect!" if metrics['total_debts'] > 0 else None
        st.metric("Pending Debts", f"₹{metrics['total_debts']:,.2f}", delta=delta_text)
    
    with col7:
        st.metric("Total Sales", metrics['total_sales_count'])
    
    with col8:
        net_position = metrics['total_revenue'] - metrics['total_debts']
        st.metric("Net Position", f"₹{net_position:,.2f}")

def display_ai_insights(username):
    """Display AI-generated business insights"""
    st.subheader("🤖 AI-Powered Insights")
    
    insights = generate_insights(username)
    
    if insights:
        for insight in insights:
            if insight['type'] == 'success':
                st.success(f"**{insight['title']}**\n\n{insight['message']}")
            elif insight['type'] == 'warning':
                st.warning(f"**{insight['title']}**\n\n{insight['message']}")
            elif insight['type'] == 'error':
                st.error(f"**{insight['title']}**\n\n{insight['message']}")
            elif insight['type'] == 'info':
                st.info(f"**{insight['title']}**\n\n{insight['message']}")
    else:
        st.info("📊 Add more sales data to receive personalized AI insights!")

def display_quick_charts(metrics):
    """Display quick overview charts"""
    st.subheader("📈 Quick Overview")
    
    sales_df = metrics['sales_df']
    
    if not sales_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily sales trend
            daily_sales = sales_df.groupby(sales_df['date'].dt.date)['total_amount'].sum().reset_index()
            daily_sales.columns = ['Date', 'Sales']
            
            fig = px.line(
                daily_sales, 
                x='Date', 
                y='Sales',
                title='Daily Sales Trend',
                labels={'Sales': 'Amount (₹)'}
            )
            fig.update_traces(line_color='#1f77b4', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Product distribution pie chart
            product_sales = sales_df.groupby('product')['total_amount'].sum().reset_index()
            product_sales = product_sales.nlargest(5, 'total_amount')  # Top 5
            
            fig = px.pie(
                product_sales, 
                values='total_amount', 
                names='product',
                title='Top 5 Products by Revenue'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Profit vs Revenue comparison
        daily_metrics = sales_df.groupby(sales_df['date'].dt.date).agg({
            'total_amount': 'sum',
            'profit': 'sum'
        }).reset_index()
        daily_metrics.columns = ['Date', 'Revenue', 'Profit']
        
        fig = px.bar(
            daily_metrics, 
            x='Date', 
            y=['Revenue', 'Profit'],
            title='Revenue vs Profit Comparison',
            barmode='group',
            labels={'value': 'Amount (₹)', 'variable': 'Type'}
        )
        st.plotly_chart(fig, use_container_width=True)

def display_welcome_message():
    """Display welcome message for new users"""
    st.info("👋 Welcome to ShopInsight Pro!")
    
    st.markdown("""
    ### Get Started in 3 Easy Steps:
    
    1. **📦 Add Inventory** - Start by adding products to your inventory
    2. **💰 Record Sales** - Log your daily sales transactions
    3. **📊 View Insights** - Get AI-powered recommendations to grow your business
    
    ### Features Available:
    - **Sales Management** - Track all sales with automatic profit calculation
    - **Inventory Tracking** - Monitor stock levels with low-stock alerts
    - **Order Management** - Keep track of pending and completed orders
    - **Debt Management** - Manage receivables and payables efficiently
    - **Advanced Analytics** - Get detailed reports and predictions
    - **AI Insights** - Receive personalized recommendations
    
    Navigate using the sidebar menu to explore all features! 🚀
    """)

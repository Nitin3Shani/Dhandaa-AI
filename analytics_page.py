"""
Advanced analytics module
Comprehensive analytics and visualizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from analytics import calculate_metrics, get_product_performance, predict_monthly_revenue
from config import TIME_PERIODS

def show_analytics_page(username):
    """Display advanced analytics page"""
    st.title("📈 Advanced Analytics")
    
    metrics = calculate_metrics(username)
    
    if not metrics:
        st.info("📊 Add sales data to view advanced analytics")
        return
    
    # Time period selector
    period = st.selectbox("Analysis Period", TIME_PERIODS)
    
    # Filter data based on period
    sales_df = filter_by_period(metrics['sales_df'], period)
    
    if sales_df.empty:
        st.warning("No data available for the selected period")
        return
    
    # Display analytics sections
    display_revenue_profit_analysis(sales_df)
    st.markdown("---")
    
    display_product_performance(username, sales_df)
    st.markdown("---")
    
    display_profit_margin_analysis(sales_df)
    st.markdown("---")
    
    display_sales_distribution(sales_df)
    st.markdown("---")
    
    display_predictive_insights(username, metrics)

def filter_by_period(sales_df, period):
    """Filter sales data by selected time period"""
    if period == "All Time":
        return sales_df
    
    days_map = {
        "Last 7 Days": 7,
        "Last 30 Days": 30,
        "Last 90 Days": 90
    }
    
    days = days_map.get(period, 30)
    cutoff_date = datetime.now() - timedelta(days=days)
    return sales_df[sales_df['date'] >= cutoff_date]

def display_revenue_profit_analysis(sales_df):
    """Display revenue and profit trend analysis"""
    st.subheader("💰 Revenue & Profit Analysis")
    
    daily_metrics = sales_df.groupby(sales_df['date'].dt.date).agg({
        'total_amount': 'sum',
        'profit': 'sum'
    }).reset_index()
    daily_metrics.columns = ['Date', 'Revenue', 'Profit']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_metrics['Date'], 
        y=daily_metrics['Revenue'],
        name='Revenue',
        mode='lines+markers',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_metrics['Date'], 
        y=daily_metrics['Profit'],
        name='Profit',
        mode='lines+markers',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Revenue vs Profit Trend',
        xaxis_title='Date',
        yaxis_title='Amount (₹)',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_product_performance(username, sales_df):
    """Display product performance metrics"""
    st.subheader("🏆 Product Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top products by revenue
        product_revenue = sales_df.groupby('product')['total_amount'].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=product_revenue.values,
            y=product_revenue.index,
            orientation='h',
            title='Top 10 Products by Revenue',
            labels={'x': 'Revenue (₹)', 'y': 'Product'},
            color=product_revenue.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top products by profit
        product_profit = sales_df.groupby('product')['profit'].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=product_profit.values,
            y=product_profit.index,
            orientation='h',
            title='Top 10 Products by Profit',
            labels={'x': 'Profit (₹)', 'y': 'Product'},
            color=product_profit.values,
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Product performance table
    product_stats = get_product_performance(username)
    if product_stats is not None:
        st.markdown("#### Detailed Product Metrics")
        st.dataframe(
            product_stats.head(10).style.background_gradient(subset=['profit_margin_%'], cmap='RdYlGn'),
            use_container_width=True
        )

def display_profit_margin_analysis(sales_df):
    """Display profit margin analysis"""
    st.subheader("📊 Profit Margin Analysis")
    
    product_margins = sales_df.groupby('product').agg({
        'total_amount': 'sum',
        'profit': 'sum'
    })
    product_margins['margin_%'] = (product_margins['profit'] / product_margins['total_amount'] * 100).round(2)
    product_margins = product_margins.sort_values('margin_%', ascending=False).head(10)
    
    fig = px.bar(
        product_margins,
        y=product_margins.index,
        x='margin_%',
        orientation='h',
        title='Top 10 Products by Profit Margin (%)',
        labels={'margin_%': 'Profit Margin (%)', 'y': 'Product'},
        color='margin_%',
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Margin distribution
    col1, col2 = st.columns(2)
    
    with col1:
        avg_margin = product_margins['margin_%'].mean()
        st.metric("Average Profit Margin", f"{avg_margin:.1f}%")
    
    with col2:
        high_margin_count = len(product_margins[product_margins['margin_%'] > 40])
        st.metric("High Margin Products (>40%)", high_margin_count)

def display_sales_distribution(sales_df):
    """Display sales distribution analysis"""
    st.subheader("📅 Sales Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Day of week analysis
        sales_df['day_of_week'] = sales_df['date'].dt.day_name()
        dow_sales = sales_df.groupby('day_of_week')['total_amount'].sum().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        )
        
        fig = px.bar(
            x=dow_sales.index,
            y=dow_sales.values,
            title='Sales by Day of Week',
            labels={'x': 'Day', 'y': 'Revenue (₹)'},
            color=dow_sales.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top products by quantity
        quantity_sales = sales_df.groupby('product')['quantity'].sum().sort_values(ascending=False).head(5)
        
        fig = px.pie(
            values=quantity_sales.values,
            names=quantity_sales.index,
            title='Top 5 Products by Quantity Sold'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sales by hour (if time data available)
    if 'hour' in sales_df.columns:
        hourly_sales = sales_df.groupby('hour')['total_amount'].sum()
        fig = px.line(
            x=hourly_sales.index,
            y=hourly_sales.values,
            title='Sales by Hour of Day',
            labels={'x': 'Hour', 'y': 'Revenue (₹)'}
        )
        st.plotly_chart(fig, use_container_width=True)

def display_predictive_insights(username, metrics):
    """Display predictive insights and projections"""
    st.subheader("🔮 Predictive Insights")
    
    sales_df = metrics['sales_df']
    
    if len(sales_df) >= 7:
        recent_avg = sales_df.tail(7)['total_amount'].mean()
        overall_avg = sales_df['total_amount'].mean()
        projected_monthly = predict_monthly_revenue(username)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Daily Revenue", f"₹{overall_avg:,.2f}")
        
        with col2:
            delta_pct = ((recent_avg/overall_avg - 1) * 100)
            st.metric(
                "Recent 7-Day Average", 
                f"₹{recent_avg:,.2f}",
                delta=f"{delta_pct:+.1f}%"
            )
        
        with col3:
            st.metric("Projected Monthly Revenue", f"₹{projected_monthly:,.2f}")
        
        # Business health summary
        st.info(f"""
        **📊 Business Health Summary:**
        
        - Your business generates an average of **₹{overall_avg:,.2f}** per sale
        - Based on recent trends, projected monthly revenue is **₹{projected_monthly:,.2f}**
        - Current profit margin: **{metrics['profit_margin']:.1f}%**
        - Total sales recorded: **{metrics['total_sales_count']}**
        
        {"✅ **Your business is trending positively!**" if delta_pct > 0 else "⚠️ **Consider promotional activities to boost sales**"}
        """)
        
        # Growth visualization
        st.markdown("#### Growth Trajectory")
        daily_cumulative = sales_df.sort_values('date').set_index('date')['total_amount'].cumsum()
        
        fig = px.area(
            x=daily_cumulative.index,
            y=daily_cumulative.values,
            title='Cumulative Revenue Growth',
            labels={'x': 'Date', 'y': 'Cumulative Revenue (₹)'}
        )
        fig.update_traces(fillcolor='rgba(46, 204, 113, 0.3)', line_color='#2ecc71')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add at least 7 days of sales data to see predictive insights")

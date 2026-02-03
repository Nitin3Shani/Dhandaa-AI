"""
Analytics module
Handles all calculations, metrics, and AI-powered insights
"""

import pandas as pd
from data_manager import get_user_data
from config import (
    LOW_PROFIT_MARGIN_THRESHOLD, 
    HIGH_PROFIT_MARGIN_THRESHOLD,
    DEBT_WARNING_RATIO,
    LOW_STOCK_THRESHOLD,
    SALES_GROWTH_THRESHOLD,
    SALES_DECLINE_THRESHOLD
)

def calculate_metrics(username):
    """Calculate all business metrics for a user"""
    sales = get_user_data(username, 'sales')
    inventory = get_user_data(username, 'inventory')
    orders = get_user_data(username, 'orders')
    debts = get_user_data(username, 'debts')
    
    if not sales:
        return None
    
    sales_df = pd.DataFrame(sales)
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    
    # Calculate totals
    total_revenue = sales_df['total_amount'].sum()
    total_cost = sales_df['cost'].sum()
    total_profit = total_revenue - total_cost
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    # Inventory value
    inventory_value = sum(item['quantity'] * item['unit_price'] for item in inventory)
    
    # Pending orders
    pending_orders_value = sum(order['amount'] for order in orders if order['status'] == 'Pending')
    
    # Total debts
    total_debts = sum(debt['amount'] for debt in debts if debt['status'] == 'Pending')
    
    return {
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'profit_margin': profit_margin,
        'inventory_value': inventory_value,
        'pending_orders': pending_orders_value,
        'total_debts': total_debts,
        'sales_df': sales_df,
        'total_sales_count': len(sales)
    }

def generate_insights(username):
    """Generate AI-powered business insights"""
    metrics = calculate_metrics(username)
    if not metrics:
        return []
    
    insights = []
    sales_df = metrics['sales_df']
    
    # Insight 1: Best selling products
    if not sales_df.empty:
        product_sales = sales_df.groupby('product')['quantity'].sum().sort_values(ascending=False)
        if len(product_sales) > 0:
            top_product = product_sales.index[0]
            top_quantity = product_sales.iloc[0]
            insights.append({
                'type': 'success',
                'title': '🏆 Top Performer',
                'message': f"'{top_product}' is your best-seller with {top_quantity} units sold!"
            })
    
    # Insight 2: Profit margin analysis
    if metrics['profit_margin'] < LOW_PROFIT_MARGIN_THRESHOLD:
        insights.append({
            'type': 'warning',
            'title': '⚠️ Low Profit Margin',
            'message': f"Your profit margin is {metrics['profit_margin']:.1f}%. Consider reviewing pricing or reducing costs."
        })
    elif metrics['profit_margin'] > HIGH_PROFIT_MARGIN_THRESHOLD:
        insights.append({
            'type': 'success',
            'title': '💰 Excellent Margins',
            'message': f"Outstanding profit margin of {metrics['profit_margin']:.1f}%! Keep up the good work."
        })
    
    # Insight 3: Sales trends
    if len(sales_df) > 7:
        recent_sales = sales_df.tail(7)['total_amount'].mean()
        older_sales = sales_df.head(7)['total_amount'].mean()
        
        if recent_sales > older_sales * SALES_GROWTH_THRESHOLD:
            growth_pct = ((recent_sales/older_sales - 1) * 100)
            insights.append({
                'type': 'success',
                'title': '📈 Growth Trend',
                'message': f"Sales are trending up! Recent average is {growth_pct:.1f}% higher."
            })
        elif recent_sales < older_sales * SALES_DECLINE_THRESHOLD:
            insights.append({
                'type': 'warning',
                'title': '📉 Declining Sales',
                'message': "Sales have decreased recently. Consider promotional activities or customer outreach."
            })
    
    # Insight 4: Debt management
    if metrics['total_debts'] > metrics['total_revenue'] * DEBT_WARNING_RATIO:
        insights.append({
            'type': 'error',
            'title': '💳 High Debt Alert',
            'message': f"Pending debts (₹{metrics['total_debts']:,.2f}) are over 30% of revenue. Prioritize collections."
        })
    
    # Insight 5: Inventory insights
    inventory = get_user_data(username, 'inventory')
    low_stock = [item for item in inventory if item['quantity'] < LOW_STOCK_THRESHOLD]
    if low_stock:
        product_names = ', '.join([item['name'] for item in low_stock[:3]])
        more_text = f" and {len(low_stock)-3} more" if len(low_stock) > 3 else ""
        insights.append({
            'type': 'warning',
            'title': '📦 Low Stock Alert',
            'message': f"{len(low_stock)} item(s) running low. Restock: {product_names}{more_text}"
        })
    
    # Insight 6: Product diversity
    if not sales_df.empty:
        unique_products = sales_df['product'].nunique()
        if unique_products < 3:
            insights.append({
                'type': 'info',
                'title': '🎯 Product Diversity',
                'message': f"You're selling {unique_products} product(s). Consider expanding your product range to attract more customers."
            })
    
    return insights

def get_product_performance(username):
    """Get detailed product performance metrics"""
    sales_df = calculate_metrics(username)
    if not sales_df or sales_df['sales_df'].empty:
        return None
    
    df = sales_df['sales_df']
    
    # Aggregate by product
    product_stats = df.groupby('product').agg({
        'quantity': 'sum',
        'total_amount': 'sum',
        'profit': 'sum'
    }).reset_index()
    
    product_stats['profit_margin_%'] = (
        product_stats['profit'] / product_stats['total_amount'] * 100
    ).round(2)
    
    return product_stats.sort_values('total_amount', ascending=False)

def predict_monthly_revenue(username):
    """Predict monthly revenue based on recent trends"""
    metrics = calculate_metrics(username)
    if not metrics:
        return 0
    
    sales_df = metrics['sales_df']
    if len(sales_df) < 7:
        return 0
    
    recent_avg = sales_df.tail(7)['total_amount'].mean()
    return recent_avg * 30

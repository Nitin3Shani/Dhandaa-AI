"""
Debts management module
Handles all debt and receivables operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_manager import get_user_data, save_user_data
from config import DEBT_STATUSES, DEBT_TYPES

def show_debts_page(username):
    """Display debts management page"""
    st.title("💳 Debts & Receivables Management")
    
    tab1, tab2 = st.tabs(["Add Debt/Receivable", "View Records"])
    
    with tab1:
        add_debt_form(username)
    
    with tab2:
        view_debts_table(username)

def add_debt_form(username):
    """Form to add a new debt record"""
    st.subheader("Record Debt/Receivable")
    
    with st.form("add_debt_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            debtor_name = st.text_input("Customer/Debtor Name*")
            amount = st.number_input("Amount (₹)*", min_value=0.0, value=0.0, step=0.01, format="%.2f")
            debt_type = st.selectbox("Type*", DEBT_TYPES)
        
        with col2:
            status = st.selectbox("Status*", DEBT_STATUSES)
            debt_date = st.date_input("Date*", value=datetime.now())
            due_date = st.date_input("Due Date*", value=datetime.now() + timedelta(days=30))
        
        notes = st.text_area("Notes (Optional)")
        
        # Show explanation
        if debt_type == "Receivable (They owe you)":
            st.info("💰 This person owes you money")
        else:
            st.warning("💳 You owe this person/company money")
        
        submitted = st.form_submit_button("Add Record", type="primary", use_container_width=True)
        
        if submitted:
            if debtor_name and amount > 0:
                debt_data = {
                    'id': len(get_user_data(username, 'debts')) + 1,
                    'debtor': debtor_name,
                    'amount': amount,
                    'type': debt_type,
                    'status': status,
                    'debt_date': str(debt_date),
                    'due_date': str(due_date),
                    'notes': notes if notes else ""
                }
                
                save_user_data(username, 'debts', debt_data)
                st.success("✅ Debt record added!")
                st.rerun()
            else:
                st.error("Please fill all required fields")

def view_debts_table(username):
    """Display debt records in a table"""
    debts = get_user_data(username, 'debts')
    
    if debts:
        df = pd.DataFrame(debts)
        
        # Convert dates
        df['debt_date'] = pd.to_datetime(df['debt_date'])
        df['due_date'] = pd.to_datetime(df['due_date'])
        
        # Calculate days until due
        df['days_to_due'] = (df['due_date'] - datetime.now()).dt.days
        
        # Format amounts
        df['amount_fmt'] = df['amount'].apply(lambda x: f"₹{x:,.2f}")
        
        # Summary cards at top
        col1, col2, col3, col4 = st.columns(4)
        
        receivables_pending = df[(df['type'] == "Receivable (They owe you)") & (df['status'] == "Pending")]['amount'].sum()
        payables_pending = df[(df['type'] == "Payable (You owe them)") & (df['status'] == "Pending")]['amount'].sum()
        total_receivables = df[df['type'] == "Receivable (They owe you)"]['amount'].sum()
        total_payables = df[df['type'] == "Payable (You owe them)"]['amount'].sum()
        
        with col1:
            st.metric("Pending Receivables", f"₹{receivables_pending:,.2f}", 
                     delta="To Collect" if receivables_pending > 0 else None)
        
        with col2:
            st.metric("Pending Payables", f"₹{payables_pending:,.2f}",
                     delta="To Pay" if payables_pending > 0 else None)
        
        with col3:
            st.metric("Total Receivables", f"₹{total_receivables:,.2f}")
        
        with col4:
            st.metric("Total Payables", f"₹{total_payables:,.2f}")
        
        st.markdown("---")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            type_filter = st.multiselect(
                "Filter by Type",
                options=DEBT_TYPES,
                default=DEBT_TYPES
            )
        
        with col2:
            status_filter = st.multiselect(
                "Filter by Status",
                options=DEBT_STATUSES,
                default=["Pending", "Partially Paid"]
            )
        
        with col3:
            sort_by = st.selectbox("Sort by", ["Due Date", "Amount", "Date Added"])
        
        # Apply filters
        filtered_df = df[(df['type'].isin(type_filter)) & (df['status'].isin(status_filter))]
        
        # Apply sorting
        if sort_by == "Due Date":
            filtered_df = filtered_df.sort_values('due_date')
        elif sort_by == "Amount":
            filtered_df = filtered_df.sort_values('amount', ascending=False)
        else:
            filtered_df = filtered_df.sort_values('debt_date', ascending=False)
        
        # Display columns
        display_df = filtered_df[['id', 'debtor', 'amount_fmt', 'type', 'status', 'debt_date', 'due_date', 'days_to_due']]
        display_df.columns = ['ID', 'Name', 'Amount', 'Type', 'Status', 'Date', 'Due Date', 'Days to Due']
        
        # Styling
        def highlight_debts(row):
            if row['Status'] == 'Pending' and row['Days to Due'] < 0:
                return ['background-color: #ffcccc'] * len(row)  # Overdue
            elif row['Status'] == 'Pending' and row['Days to Due'] <= 7:
                return ['background-color: #fff4cc'] * len(row)  # Due soon
            elif row['Status'] == 'Paid':
                return ['background-color: #ccffcc'] * len(row)  # Paid
            return [''] * len(row)
        
        st.dataframe(
            display_df.style.apply(highlight_debts, axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        st.caption("🔴 Overdue | 🟡 Due Soon (7 days) | 🟢 Paid")
        
        # Detailed breakdown
        st.markdown("---")
        st.subheader("📊 Breakdown by Type")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Receivables (They owe you)**")
            receivables_df = df[df['type'] == "Receivable (They owe you)"]
            if not receivables_df.empty:
                rec_summary = receivables_df.groupby('status')['amount'].sum()
                for status, amount in rec_summary.items():
                    st.write(f"- {status}: ₹{amount:,.2f}")
            else:
                st.write("No receivables")
        
        with col2:
            st.markdown("**Payables (You owe them)**")
            payables_df = df[df['type'] == "Payable (You owe them)"]
            if not payables_df.empty:
                pay_summary = payables_df.groupby('status')['amount'].sum()
                for status, amount in pay_summary.items():
                    st.write(f"- {status}: ₹{amount:,.2f}")
            else:
                st.write("No payables")
        
        # Download option
        st.markdown("---")
        csv = pd.DataFrame(debts).to_csv(index=False)
        st.download_button(
            label="📥 Download Debts Data (CSV)",
            data=csv,
            file_name=f"debts_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No debt records yet. Add your first record above!")

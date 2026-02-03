"""
Authentication module
Handles user login, registration, and session management
"""

import streamlit as st
from datetime import datetime
from data_manager import load_json, save_json, hash_password
from config import USERS_FILE, BUSINESSES_FILE, SALES_FILE, INVENTORY_FILE, ORDERS_FILE, DEBTS_FILE, BUSINESS_TYPES

def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'business_name' not in st.session_state:
        st.session_state.business_name = None

def login_user(username, password):
    """Authenticate user and return user type"""
    users = load_json(USERS_FILE)
    if username in users and users[username]["password"] == hash_password(password):
        return True, users[username]["type"], users[username].get("business_name", "Admin")
    return False, None, None

def register_user(username, password, business_name, business_type):
    """Register a new user"""
    users = load_json(USERS_FILE)
    
    if username in users:
        return False, "Username already exists"
    
    # Create user account
    users[username] = {
        "password": hash_password(password),
        "type": "user",
        "business_name": business_name,
        "business_type": business_type,
        "created_at": str(datetime.now())
    }
    save_json(USERS_FILE, users)
    
    # Initialize business data
    businesses = load_json(BUSINESSES_FILE)
    businesses[username] = {
        "name": business_name,
        "type": business_type,
        "created_at": str(datetime.now())
    }
    save_json(BUSINESSES_FILE, businesses)
    
    # Initialize empty data collections for this user
    for file in [SALES_FILE, INVENTORY_FILE, ORDERS_FILE, DEBTS_FILE]:
        data = load_json(file)
        data[username] = []
        save_json(file, data)
    
    return True, "Registration successful!"

def show_login_page():
    """Display login and registration page"""
    st.title("🏪 ShopInsight Pro")
    st.subheader("Business Analytics & Management Platform")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Login", type="primary", use_container_width=True):
                if username and password:
                    success, user_type, business_name = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_type = user_type
                        st.session_state.username = username
                        st.session_state.business_name = business_name
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please fill all fields")
        
            
    with tab2:
        st.markdown("### Register Your Business")
        
        with st.form("registration_form"):
            new_username = st.text_input("Username*")
            new_password = st.text_input("Password*", type="password")
            confirm_password = st.text_input("Confirm Password*", type="password")
            business_name = st.text_input("Business Name*")
            business_type = st.selectbox("Business Type*", BUSINESS_TYPES)
            
            submitted = st.form_submit_button("Register", type="primary", use_container_width=True)
            
            if submitted:
                if all([new_username, new_password, confirm_password, business_name]):
                    if new_password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, message = register_user(new_username, new_password, business_name, business_type)
                        if success:
                            st.success(message)
                            st.info("Please switch to the Login tab to sign in")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill all required fields")

import streamlit as st
from auth import show_login_page, init_session_state
from admin_dashboard import show_admin_dashboard
from user_dashboard import show_user_dashboard

# Set page config
st.set_page_config(page_title="Dhandaa AI", layout="wide", page_icon="📊")

# Initialize session state
init_session_state()

def main():
    """Main application entry point"""
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.user_type == "admin":
            show_admin_dashboard()
        else:
            show_user_dashboard()

if __name__ == "__main__":
    main()

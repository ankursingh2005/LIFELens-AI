import streamlit as st
import os
from database import init_database, create_user, verify_user, get_user_demographics
from auth import hash_password, verify_password, validate_email
import pages.home as home
import pages.demographics as demographics
import pages.upload_analyze as upload_analyze
import pages.diet_chart as diet_chart
import pages.reports as reports

# Initialize the database
init_database()

# Set page configuration
st.set_page_config(
    page_title="LIFELens-AI: Kidney Health Monitoring",
    page_icon="🫘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

def show_login_signup():
    """Display login and signup forms"""
    st.title("🫘 LIFELens-AI")
    st.subheader("Intelligent Kidney Health Monitoring and Assistance")
    
    # Create tabs for login and signup
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
    
    with login_tab:
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if email and password:
                    if validate_email(email):
                        user = verify_user(email, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.username = email
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.error("Please enter a valid email address")
                else:
                    st.error("Please fill in all fields")
    
    with signup_tab:
        st.header("Sign Up")
        with st.form("signup_form"):
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            full_name = st.text_input("Full Name")
            signup_button = st.form_submit_button("Sign Up")
            
            if signup_button:
                if all([new_email, new_password, confirm_password, full_name]):
                    if validate_email(new_email):
                        if new_password == confirm_password:
                            if len(new_password) >= 6:
                                success, message = create_user(new_email, new_password, full_name)
                                if success:
                                    st.success("Account created successfully! Please login.")
                                else:
                                    st.error(message)
                            else:
                                st.error("Password must be at least 6 characters long")
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.error("Please enter a valid email address")
                else:
                    st.error("Please fill in all fields")

def show_sidebar():
    """Display sidebar navigation"""
    with st.sidebar:
        st.title("🫘 LIFELens-AI")
        st.write(f"Welcome, {st.session_state.username}")
        
        # Navigation menu
        pages = ["Home", "Demographics", "Upload & Analyze", "Diet Chart", "Reports"]
        
        for page in pages:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.divider()
        
        # Logout button
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = "Home"
            st.rerun()

def main():
    """Main application logic"""
    if not st.session_state.logged_in:
        show_login_signup()
    else:
        show_sidebar()
        
        # Display the selected page
        if st.session_state.current_page == "Home":
            home.show_page()
        elif st.session_state.current_page == "Demographics":
            demographics.show_page()
        elif st.session_state.current_page == "Upload & Analyze":
            upload_analyze.show_page()
        elif st.session_state.current_page == "Diet Chart":
            diet_chart.show_page()
        elif st.session_state.current_page == "Reports":
            reports.show_page()

if __name__ == "__main__":
    main()

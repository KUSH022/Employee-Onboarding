import json
import os
import pandas as pd
import streamlit as st

USERS_FILE = os.path.join("data", "users.json")
EMPLOYEES_FILE = os.path.join("data", "employees", "employees.csv")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def get_employee_by_id(emp_id):
    """Fetch profile from employees.csv based on Employee ID."""
    if not os.path.exists(EMPLOYEES_FILE):
        return None
    
    try:
        df = pd.read_csv(EMPLOYEES_FILE)
        # Ensure Employee ID is treated as string for matching
        df["Employee ID"] = df["Employee ID"].astype(str)
        match = df[df["Employee ID"] == str(emp_id)]
        if not match.empty:
            return match.iloc[0].to_dict()
    except Exception as e:
        print(f"Error reading employees.csv: {e}")
    
    return None

def authenticate_by_id(emp_id):
    emp_details = get_employee_by_id(emp_id)
    if not emp_details:
        return None
    
    # Sync with users.json
    users = load_users()
    user_exists = False
    for user in users:
        if str(user.get("Employee ID")) == str(emp_id):
            user_exists = True
            user.update(emp_details) # Update any changed info from CSV
            break
            
    if not user_exists:
        # Create a new user record
        new_user = emp_details.copy()
        new_user["username"] = str(emp_id) # Use ID as unique username for file storage
        users.append(new_user)
        save_users(users)
        
    return emp_details

def login_page():
    # Native Streamlit Centering
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.markdown("<div style='text-align: center; margin-bottom: 2rem;'>", unsafe_allow_html=True)
        st.title("🏢 Employee Portal")
        st.subheader("Sign In")
        st.markdown("</div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            with st.form("login_form", border=False):
                emp_id = st.text_input("Enter Your Employee ID", placeholder="e.g. 101")
                submit = st.form_submit_button("Access Portal", use_container_width=True)
                
                if submit:
                    if not emp_id:
                        st.warning("Please enter your ID.")
                    else:
                        user = authenticate_by_id(emp_id)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            # Store ID as username for compatibility with chat_manager
                            st.session_state.user["username"] = str(emp_id)
                            st.success(f"Identity Verified: Welcome, {user['Name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid Employee ID. Please check your credentials.")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.current_chat_id = None
    st.rerun()

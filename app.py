import os
import streamlit as st
from auth import login_page, logout
from chat_manager import load_chats, create_new_chat, delete_chat, update_chat_messages, get_chat_by_id
from rag_pipeline import RAGPipeline
from utils import show_toast, display_chat_message, inject_autoscroll, show_typing_indicator

# ------------------ SETUP ------------------
st.set_page_config(
    page_title="Enterprise Onboarding Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    if os.path.exists("styles/style.css"):
        with open("styles/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
inject_autoscroll()

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "rag" not in st.session_state:
    st.session_state.rag = None

# Initialize RAG Pipeline (Singleton)
if st.session_state.logged_in and st.session_state.rag is None:
    try:
        with st.spinner("🚀 Preparing HR Knowledge base..."):
            st.session_state.rag = RAGPipeline()
    except Exception as e:
        st.error(f"Failed to start RAG: {e}")

# ------------------ MAIN LOGIC ------------------
if not st.session_state.logged_in:
    login_page()
else:
    user = st.session_state.user # User now has Name, Role, Department, Employee ID
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown(f"### 🏢 Portal")
        st.markdown("---")
        
        # New Chat Button
        if st.button("➕ Start New Discussion", use_container_width=True, type="primary"):
            chat_id = create_new_chat(user["username"])
            st.session_state.current_chat_id = chat_id
            st.rerun()
            
        st.markdown("### Recent Activity")
        chats = load_chats(user["username"])
        
        if not chats:
            st.info("No discussions yet.")
        
        for chat in chats:
            is_active = st.session_state.current_chat_id == chat["chat_id"]
            
            col1, col2 = st.columns([8, 2])
            with col1:
                label = f"💬 {chat['title']}"
                if st.button(label, key=f"btn_{chat['chat_id']}", use_container_width=True, disabled=is_active):
                    st.session_state.current_chat_id = chat["chat_id"]
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{chat['chat_id']}", help="Delete Chat"):
                    delete_chat(user["username"], chat["chat_id"])
                    if st.session_state.current_chat_id == chat["chat_id"]:
                        st.session_state.current_chat_id = None
                    show_toast("Thread removed", "success")
                    st.rerun()
        
        # --- USER PROFILE CARD ---
        st.markdown("---")
        st.markdown(f"""
        <div style="background: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <p style="margin:0; font-size: 0.75rem; text-transform: uppercase; color: #6c757d; font-weight: 600;">Signed in as</p>
            <div style="margin-top: 5px;">
                <strong style="font-size: 1.1rem; color: #002D62;">{user.get('Name')}</strong>
            </div>
            <p style="margin:2px 0; font-size: 0.85rem; color: #495057;"><strong>{user.get('Role')}</strong> • {user.get('Department')}</p>
            <p style="margin:0; font-size: 0.7rem; color: #adb5bd;">ID: {user.get('Employee ID')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Log Out", use_container_width=True):
            logout()

    # --- MAIN CHAT WINDOW ---
    if not st.session_state.current_chat_id:
        # Dashboard Header (Personalized)
        st.markdown("<div style='text-align: center; padding-top: 2rem;'>", unsafe_allow_html=True)
        st.title(f"💼 Welcome, {user.get('Name')}")
        st.markdown(f"**{user.get('Role')}** | {user.get('Department')}")
        st.write("I am your AI assistant for enterprise onboarding. How can I help you today?")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Dashboard Cards
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("### Common Inquiries")
        colA, colB, colC = st.columns(3)
        
        q1 = "Remote Work Policy"
        q2 = "Employee Benefits"
        q3 = "Annual Leave Details"
        
        if colA.button(f"🏢 {q1}", use_container_width=True):
            chat_id = create_new_chat(user["username"])
            st.session_state.current_chat_id = chat_id
            curr_chat = get_chat_by_id(user["username"], chat_id)
            curr_chat["messages"].append({"role": "user", "content": q1})
            update_chat_messages(user["username"], chat_id, curr_chat["messages"])
            st.rerun()
            
        if colB.button(f"🎁 {q2}", use_container_width=True):
            chat_id = create_new_chat(user["username"])
            st.session_state.current_chat_id = chat_id
            curr_chat = get_chat_by_id(user["username"], chat_id)
            curr_chat["messages"].append({"role": "user", "content": q2})
            update_chat_messages(user["username"], chat_id, curr_chat["messages"])
            st.rerun()
            
        if colC.button(f"🏖️ {q3}", use_container_width=True):
            chat_id = create_new_chat(user["username"])
            st.session_state.current_chat_id = chat_id
            curr_chat = get_chat_by_id(user["username"], chat_id)
            curr_chat["messages"].append({"role": "user", "content": q3})
            update_chat_messages(user["username"], chat_id, curr_chat["messages"])
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        current_chat = get_chat_by_id(user["username"], st.session_state.current_chat_id)
        if current_chat:
            st.markdown(f"## 💬 {current_chat['title']}")
            st.divider()
            for msg in current_chat["messages"]:
                display_chat_message(msg["role"], msg["content"])
            
            # Auto-respond logic
            if current_chat["messages"] and current_chat["messages"][-1]["role"] == "user":
                prompt = current_chat["messages"][-1]["content"]
                with st.spinner("🧠 Analyzing policies..."):
                    try:
                        response = st.session_state.rag.get_response(
                            query=prompt, 
                            chat_history=current_chat["messages"][:-1],
                            role=user.get("Role", "Employee"),
                            name=user.get("Name", "User")
                        )
                        display_chat_message("assistant", response)
                        current_chat["messages"].append({"role": "assistant", "content": response})
                        update_chat_messages(user["username"], st.session_state.current_chat_id, current_chat["messages"])
                        st.rerun()
                    except Exception as e:
                        st.error("API Connection Error")
            
            if next_prompt := st.chat_input("👋 Type your HR question here..."):
                display_chat_message("user", next_prompt)
                current_chat["messages"].append({"role": "user", "content": next_prompt})
                update_chat_messages(user["username"], st.session_state.current_chat_id, current_chat["messages"])
                st.rerun()

import streamlit as st

def inject_autoscroll():
    """Injects JavaScript to keep the chat scrolled to the bottom."""
    js = """
    <script>
        function scrollToBottom() {
            const chatMain = window.parent.document.querySelector('section.main');
            if (chatMain) {
                chatMain.scrollTop = chatMain.scrollHeight;
            }
        }
        // Run on load and periodically
        scrollToBottom();
        window.parent.document.addEventListener('DOMNodeInserted', scrollToBottom);
    </script>
    """
    st.components.v1.html(js, height=0)


def show_toast(message, type="info"):
    icon = "✅" if type == "success" else "❌" if type == "error" else "ℹ️"
    st.toast(f"{icon} {message}")

def display_chat_message(role, content):
    with st.chat_message(role):
        st.markdown(content)

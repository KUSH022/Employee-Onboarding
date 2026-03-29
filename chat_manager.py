import json
import os
import uuid
from datetime import datetime

CHATS_DIR = os.path.join("data", "chats")

def get_chat_file(username):
    return os.path.join(CHATS_DIR, f"{username}.json")

def load_chats(username):
    file_path = get_chat_file(username)
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)

def save_chats(username, chats):
    file_path = get_chat_file(username)
    with open(file_path, "w") as f:
        json.dump(chats, f, indent=4)

def create_new_chat(username):
    chat_id = str(uuid.uuid4())
    new_chat = {
        "chat_id": chat_id,
        "title": f"New Chat {datetime.now().strftime('%H:%M')}",
        "messages": [],
        "created_at": datetime.now().isoformat()
    }
    
    chats = load_chats(username)
    chats.insert(0, new_chat)
    save_chats(username, chats)
    return chat_id

def delete_chat(username, chat_id):
    chats = load_chats(username)
    chats = [c for c in chats if c["chat_id"] != chat_id]
    save_chats(username, chats)

def update_chat_messages(username, chat_id, messages):
    chats = load_chats(username)
    for chat in chats:
        if chat["chat_id"] == chat_id:
            chat["messages"] = messages
            # Update title from first query if still "New Chat"
            if len(messages) >= 1 and "New Chat" in chat["title"]:
                first_query = messages[0]["content"]
                chat["title"] = (first_query[:30] + '...') if len(first_query) > 30 else first_query
            break
    save_chats(username, chats)

def get_chat_by_id(username, chat_id):
    chats = load_chats(username)
    for chat in chats:
        if chat["chat_id"] == chat_id:
            return chat
    return None

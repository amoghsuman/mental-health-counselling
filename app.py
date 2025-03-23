import streamlit as st
from datetime import datetime

# Page configuration and UI cleanup
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠", layout="wide")
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)  # Hide Streamlit menu & footer&#8203;:contentReference[oaicite:3]{index=3}

# Initialize session state for chat history and input, if not already set
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list to hold messages (with role, text, timestamp)
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""    # current text in the chat input field

# Top section: Mode and Mood selection
st.title("Mental Health Chatbot")
mode = st.selectbox("Mode:", ["Therapy Mode", "Casual Mode"], key="mode_select")
mood = st.selectbox("Mood:", ["🙂 Happy", "😢 Sad", "😟 Anxious", "😠 Angry", "😕 Confused"], key="mood_select")

# Define callback functions for sending message and clearing chat
def send_message():
    """Callback when user sends a message (via Enter key or Send button)."""
    user_text = st.session_state.chat_input.strip()
    if user_text:
        # Append the user's message to chat history with timestamp
        st.session_state.chat_history.append({
            "role": "user", 
            "text": user_text, 
            "time": datetime.now().strftime("%H:%M")
        })
        # (Optional) Generate bot response here and append to history
        # For example, a simple echo response (replace this with real model call):
        bot_reply = f"You said: {user_text}"
        st.session_state.chat_history.append({
            "role": "bot", 
            "text": bot_reply, 
            "time": datetime.now().strftime("%H:%M")
        })
    # Clear the input field after sending
    st.session_state.chat_input = ""  # safe to modify inside callback&#8203;:contentReference[oaicite:4]{index=4}

def clear_chat():
    """Callback to clear the conversation history."""
    st.session_state.chat_history = []
    st.session_state.chat_input = ""

# ChatBar: Text input and Send button at the top of the chat
input_col, send_col, clear_col = st.columns([0.8, 0.1, 0.1])
with input_col:
    st.text_input(
        "Type your message", 
        value=st.session_state.chat_input, 
        key="chat_input", 
        placeholder="Type a message and press Enter", 
        on_change=send_message, 
        label_visibility="collapsed"
    )
with send_col:
    st.button("✈️ Send", on_click=send_message)
with clear_col:
    st.button("🗑️ Clear Chat", on_click=clear_chat)

# Display chat history with emojis and timestamps
st.divider()  # horizontal line separator
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"🙂 **You:** {msg['text']}  \n*{msg['time']}*")
    else:
        st.markdown(f"🤖 **Bot:** {msg['text']}  \n*{msg['time']}*")

# Custom footer branding at the bottom
st.markdown("---", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color: gray; font-size:0.9rem;'>"
    "© 2025 Your Company Name &mdash; All rights reserved."
    "</div>",
    unsafe_allow_html=True
)

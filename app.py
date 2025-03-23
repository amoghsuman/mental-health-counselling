import streamlit as st
from chatbot import get_chatbot_response

st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="centered")
st.title("🧠 Mental Health Support Chatbot")

# Mode selector
mode = st.selectbox("Choose your support style:", ["Therapist", "Friend", "Coach"])
st.markdown("Feel free to express what's on your mind. I'm here to listen. 💙")

# Initialize chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Message input
user_input = st.text_input("Type your message here...")

# Handle response
# Store message pairs
if st.button("Send") and user_input:
    response = get_chatbot_response(user_input, mode=mode)
    st.session_state.chat_history.append((
        ("You", user_input),
        ("Chatbot", response)
    ))

# Emoji/avatar mapping
SPEAKER_MAP = {
    "You": {"role": "user", "emoji": "🧑‍💻"},
    "Chatbot": {"role": "assistant", "emoji": {
        "Therapist": "🧠", "Friend": "👭", "Coach": "💼"
    }.get(mode, "🧠")}
}

# Display chat messages (latest on top)
# Display in reverse, preserving user-bot sequence
for user_msg, bot_msg in reversed(st.session_state.chat_history):
    for speaker, msg in [user_msg, bot_msg]:
        meta = SPEAKER_MAP.get(speaker, {"role": "assistant", "emoji": "🤖"})
        with st.chat_message(meta["role"]):
            st.markdown(f"{meta['emoji']} **{speaker}:** {msg}")
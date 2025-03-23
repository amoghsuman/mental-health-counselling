import streamlit as st
from chatbot import get_chatbot_response
from datetime import datetime

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

# After button press
if st.button("Send") and user_input:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with st.spinner("Chatbot is typing..."):
        response = get_chatbot_response(user_input, mode=mode)
    st.session_state.chat_history.append((
        ("You", user_input, now),
        ("Chatbot", response, now)
    ))

# Emoji/avatar mapping by role
SPEAKER_MAP = {
    "You": {"role": "user", "emoji": "🧑‍💻"},
    "Chatbot": {
        "role": "assistant",
        "emoji": {
            "Therapist": "🧠",
            "Friend": "👭",
            "Coach": "💼"
        }.get(mode, "🧠")
    }
}

# Display chat messages (latest on top, user followed by bot)
# Display loop
for user_msg, bot_msg in reversed(st.session_state.chat_history):
    for speaker_msg in [user_msg, bot_msg]:
        speaker, msg, ts = speaker_msg
        meta = SPEAKER_MAP.get(speaker, {"role": "assistant", "emoji": "🤖"})
        with st.chat_message(meta["role"]):
            st.markdown(f"{meta['emoji']} **{speaker}** _(at {ts})_: {msg}")
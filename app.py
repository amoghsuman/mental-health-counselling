import streamlit as st
from datetime import datetime
from chatbot import get_chatbot_response

# --- Page Setup ---
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="centered")
st.title("🧠 Mental Health Support Chatbot")

# --- Load Custom Styles ---
#def load_custom_css(file_path):
 #   with open(file_path) as f:
  #      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#load_custom_css("styles.css")

# --- Mode Switcher ---
mode = st.selectbox("Choose your support style:", ["Therapist", "Friend", "Coach"])
st.markdown("Feel free to express what's on your mind. I'm here to listen. 💙")

# --- Initialize Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- User Input ---
user_input = st.text_input("Type your message here...")

# --- Handle Message Send ---
if st.button("Send") and user_input:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with st.spinner("Chatbot is typing..."):
        response = get_chatbot_response(user_input, mode=mode)
    # Store conversation pair with timestamps
    st.session_state.chat_history.append((
        ("You", user_input, now),
        ("Chatbot", response, now)
    ))

# --- Speaker Info (Emoji & Roles) ---
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

# --- Display Chat History (newest on top) ---
for user_msg, bot_msg in reversed(st.session_state.chat_history):
    for speaker_msg in [user_msg, bot_msg]:
        # Handle old 2-tuple format
        if len(speaker_msg) == 3:
            speaker, msg, ts = speaker_msg
        else:
            speaker, msg = speaker_msg
            ts = "earlier"
        meta = SPEAKER_MAP.get(speaker, {"role": "assistant", "emoji": "🤖"})
        with st.chat_message(meta["role"]):
            st.markdown(f"{meta['emoji']} **{speaker}** _(at {ts})_: {msg}")

import streamlit as st
from datetime import datetime
from chatbot import get_chatbot_response

# Set page settings
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="centered")
st.title("🧠 Mental Health Support Chatbot")

# 💻 Dark Mode CSS Styling
dark_mode_css = """
<style>
body {
    background-color: #121212;
    color: #FFFFFF;
}

[data-testid="stAppViewContainer"] {
    background-color: #121212;
}

[data-testid="stMarkdownContainer"] {
    font-size: 16px;
    padding: 8px;
    border-radius: 10px;
}

h1 {
    color: #00FFCC;
}
</style>
"""
st.markdown(dark_mode_css, unsafe_allow_html=True)

# 🎛️ Mode selector
mode = st.selectbox("Choose your support style:", ["Therapist", "Friend", "Coach"])
st.markdown("Feel free to express what's on your mind. I'm here to listen. 💙")

# 📦 Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 📝 Input section
user_input = st.text_input("Type your message here...")

# 🚀 Handle input and generate response
if st.button("Send") and user_input:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with st.spinner("Chatbot is typing..."):
        response = get_chatbot_response(user_input, mode=mode)
    # Store as a pair with timestamps
    st.session_state.chat_history.append((
        ("You", user_input, now),
        ("Chatbot", response, now)
    ))

# 🧠 Speaker metadata for display
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

# 💬 Display chat history (newest at top)
for user_msg, bot_msg in reversed(st.session_state.chat_history):
    for speaker_msg in [user_msg, bot_msg]:
        # Handle both 2-item and 3-item formats
        if len(speaker_msg) == 3:
            speaker, msg, ts = speaker_msg
        else:
            speaker, msg = speaker_msg
            ts = "earlier"

        meta = SPEAKER_MAP.get(speaker, {"role": "assistant", "emoji": "🤖"})
        with st.chat_message(meta["role"]):
            st.markdown(f"{meta['emoji']} **{speaker}** _(at {ts})_: {msg}")

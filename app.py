import streamlit as st
from datetime import datetime
from chatbot import get_chatbot_response

# --- Page Config ---
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="centered")
st.title("🧠 Mental Health Support Chatbot")

# --- Hide GitHub icon, footer, and "Hosted with Streamlit" ---
clean_ui_css = """
    <style>
    [data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    footer {
        visibility: hidden !important;
        height: 0px !important;
    }
    footer:after {
        display: none !important;
    }
    .css-164nlkn.egzxvld1, .css-cio0dv.e1tzin5v2 {
        visibility: hidden !important;
        height: 0px !important;
        display: none !important;
    }
    .block-container {
        padding-bottom: 0rem !important;
    }
    </style>
"""
st.markdown(clean_ui_css, unsafe_allow_html=True)

# --- Init Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "clear_chat_triggered" not in st.session_state:
    st.session_state.clear_chat_triggered = False

# --- Mode & Mood ---
mode = st.selectbox("Choose your support style:", ["Therapist", "Friend", "Coach"])
mood = st.radio(
    "How are you feeling right now?",
    ["😊 Happy", "😔 Sad", "😡 Angry", "😨 Anxious", "😐 Neutral"],
    horizontal=True
)
mood_label = mood.split(" ")[1]
st.markdown(f"🧭 Current mood: **{mood}**")

# --- Message Handler ---
def handle_message(clear_input=True):
    user_input = st.session_state.input_text
    if user_input:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with st.spinner("Chatbot is typing..."):
            response = get_chatbot_response(user_input, mode=mode, mood=mood_label)
        st.session_state.chat_history.append((
            ("You", user_input, now),
            ("Chatbot", response, now)
        ))
        if clear_input:
            st.session_state["input_text"] = ""

# --- Input Bar (Now at the top of the chat section) ---
col3, col4 = st.columns([6, 1])
with col3:
    st.text_input(
        "Type your message here...",
        key="input_text",
        on_change=handle_message,
        placeholder="Type something to share what's on your mind...",
        label_visibility="collapsed"
    )
with col4:
    if st.button("✈️", key="send_icon"):
        handle_message(clear_input=False)

# --- Top Buttons (Send + Clear Chat) ---
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("📝 Send"):
        handle_message(clear_input=False)
with col2:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.input_text = ""
        st.session_state.clear_chat_triggered = True

# --- Safe rerun after Clear Chat ---
if st.session_state.get("clear_chat_triggered"):
    st.session_state.clear_chat_triggered = False
    st.stop()
    st.experimental_rerun()

# --- Chat Display (Newest on Top) ---
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

for user_msg, bot_msg in reversed(st.session_state.chat_history):
    for speaker_msg in [user_msg, bot_msg]:
        if len(speaker_msg) == 3:
            speaker, msg, ts = speaker_msg
        else:
            speaker, msg = speaker_msg
            ts = "earlier"
        meta = SPEAKER_MAP.get(speaker, {"role": "assistant", "emoji": "🤖"})
        with st.chat_message(meta["role"]):
            st.markdown(f"{meta['emoji']} **{speaker}** _(at {ts})_: {msg}")

# --- Custom Footer ---
custom_footer = """
<div style='text-align: center; padding: 1rem 0; font-size: 14px; color: #888;'>
    Powered by <strong>Grant Thornton</strong> | Built with 💙 by <strong>Amogh Suman</strong>
</div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)

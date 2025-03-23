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
if "clear_chat" not in st.session_state:
    st.session_state.clear_chat = False

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
def handle_message():
    user_input = st.session_state.get("input_text", "").strip()
    if user_input:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with st.spinner("Chatbot is typing..."):
            response = get_chatbot_response(user_input, mode=mode, mood=mood_label)
        st.session_state.chat_history.append({
            "role": "user",
            "text": user_input,
            "time": now
        })
        st.session_state.chat_history.append({
            "role": "bot",
            "text": response,
            "time": now
        })
    st.session_state["input_text"] = ""  # Safely reset inside callback

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.input_text = ""

# --- Input Bar (at top of chat area) ---
col3, col4, col5 = st.columns([6, 1, 1])
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
        handle_message()
with col5:
    if st.button("🧹 Clear Chat"):
        clear_chat()

# --- Chat Display (Newest on Top) ---
for message in reversed(st.session_state.chat_history):
    role = message.get("role", "bot")
    text = message.get("text", "")
    ts = message.get("time", "earlier")

    meta = {
        "user": {"role": "user", "emoji": "🧑‍💻"},
        "bot": {
            "role": "assistant",
            "emoji": {
                "Therapist": "🧠",
                "Friend": "👭",
                "Coach": "💼"
            }.get(mode, "🧠")
        }
    }.get(role, {"role": "assistant", "emoji": "🤖"})

    with st.chat_message(meta["role"]):
        st.markdown(f"{meta['emoji']} **{role.capitalize()}** _(at {ts})_: {text}")

# --- Custom Footer ---
custom_footer = """
<div style='text-align: center; padding: 1rem 0; font-size: 14px; color: #888;'>
    Powered by <strong>Grant Thornton</strong> | Built with 💙 by <strong>Amogh Suman</strong>
</div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)

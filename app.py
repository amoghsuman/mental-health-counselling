import streamlit as st
from datetime import datetime
from chatbot import get_chatbot_response

# --- Page Config ---
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="centered")
st.title("🧠 Mental Health Support Chatbot")

# --- Clean UI: Hide GitHub icon and footer ---
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

# --- Mode & Mood ---
mode = st.selectbox("Choose your support style:", ["Therapist", "Friend", "Coach"])
mood = st.radio(
    "How are you feeling right now?",
    ["😊 Happy", "😔 Sad", "😡 Angry", "😨 Anxious", "😐 Neutral"],
    horizontal=True
)
mood_label = mood.split(" ")[1]
st.markdown(f"🧭 Current mood: **{mood}**")

# --- Init chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Handle message ---
def handle_message():
    user_input = st.session_state.input_text
    if user_input:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with st.spinner("Chatbot is typing..."):
            response = get_chatbot_response(user_input, mode=mode, mood=mood_label)
        st.session_state.chat_history.append((
            ("You", user_input, now),
            ("Chatbot", response, now)
        ))
        st.session_state["input_text"] = ""

# --- Top Buttons: Send + Clear Chat ---
col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("📝 Send"):
        handle_message()
with col_b:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.input_text = ""
        st.session_state.clear_chat_triggered = True

# --- Safe rerun after Clear Chat ---
if st.session_state.get("clear_chat_triggered"):
    st.session_state.clear_chat_triggered = False
    st.experimental_rerun()

# --- Display Chat (latest on top) ---
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

# --- Sticky Input with Send Icon ---
sticky_input_css = """
<style>
.sticky-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #fff;
    padding: 10px 15px;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
    z-index: 100;
}
.input-row {
    display: flex;
    gap: 10px;
}
.input-row input {
    flex: 1;
    padding: 0.6rem;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ccc;
}
.input-row button {
    padding: 0.6rem 1rem;
    font-size: 18px;
    background-color: #00C853;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.block-container {
    padding-bottom: 90px !important;
}
</style>
"""
st.markdown(sticky_input_css, unsafe_allow_html=True)

# --- Render Sticky Input UI ---
st.markdown("<div class='sticky-container'><div class='input-row'>", unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])
with col1:
    st.text_input("Type your message here...", key="input_text", on_change=handle_message, label_visibility="collapsed")
with col2:
    if st.button("✈️", key="send_icon"):
        handle_message()
st.markdown("</div></div>", unsafe_allow_html=True)

# --- Custom Footer ---
custom_footer = """
<div style='text-align: center; padding: 1rem 0; font-size: 14px; color: #888;'>
    Powered by <strong>Grant Thornton</strong> | Built with 💙 by <strong>Amogh Suman</strong>
</div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)

import streamlit as st
from datetime import datetime
from chatbot import get_chatbot_response

# --- Page Config ---
st.set_page_config(page_title="🧠 Mental Health Assistant", layout="centered")
st.title("🧠 Mental Health Counselling Assistant")

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
if "clear_chat_flag" not in st.session_state:
    st.session_state.clear_chat_flag = False
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "send_button_pressed" not in st.session_state:
    st.session_state.send_button_pressed = False
if "reset_input_flag" not in st.session_state:
    st.session_state.reset_input_flag = False

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
def handle_message(clear_input=False):
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
        if clear_input:
            st.session_state.input_text = ""  # ✅ Safe inside on_change

# --- Clear Chat Handler ---
def clear_chat():
    st.session_state.clear_chat_flag = True

# --- Input Bar (at top of chat area) ---
col3, col4, col5 = st.columns([6, 1, 1])
with col3:
    st.text_input(
        "Type your message here...",
        key="input_text",
        on_change=lambda: handle_message(clear_input=True),
        placeholder="Tell me what's on your mind...",
        label_visibility="collapsed"
    )
with col4:
    if st.button("✈️ Send", key="send_icon"):
        st.session_state.send_button_pressed = True
with col5:
    if st.button("🧹 Clear Chat"):
        clear_chat()

# --- Handle Send Button After Widgets Rendered ---
if st.session_state.send_button_pressed:
    handle_message(clear_input=False)  # ❌ Don't clear directly
    st.session_state.send_button_pressed = False
    st.session_state.reset_input_flag = True  # ✅ Triggers safe rerun reset

# --- Reset input_text safely via rerun ---
if st.session_state.reset_input_flag:
    st.session_state.reset_input_flag = False
    st.rerun()

# --- Chat Display (Newest on Top) ---
# --- Chat Display (Newest pairs on top, User above Bot) ---
pairs = list(zip(st.session_state.chat_history[::2], st.session_state.chat_history[1::2]))
for user_msg, bot_msg in reversed(pairs):
    for msg in [user_msg, bot_msg]:
        role = msg.get("role", "bot")
        text = msg.get("text", "")
        ts = msg.get("time", "earlier")

        name = "User" if role == "user" else mode  # Show role as 'Therapist', 'Friend', or 'Coach'

        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(f"**{name}** _(at {ts})_: {text}")



# --- Safe Clear Chat Rerun ---
if st.session_state.clear_chat_flag:
    st.session_state.chat_history = []
    st.session_state.clear_chat_flag = False
    st.rerun()

# --- Custom Footer ---
custom_footer = """
<div style='text-align: center; padding: 1rem 0; font-size: 14px; color: #888;'>
    Powered by <strong>Grant Thornton</strong> | Built with 💙 by <strong>Amogh Suman</strong>
</div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)

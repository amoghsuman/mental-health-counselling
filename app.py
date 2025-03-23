import streamlit as st
from datetime import datetime
from chatbot import get_chatbot_response

# --- Page Config ---
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="centered")
st.title("🧠 Mental Health Support Chatbot")

# --- Hide GitHub icon, menu, and footer on all devices (mobile & desktop) ---
clean_ui_css = """
    <style>
        /* Hide top-right toolbar (GitHub icon, hamburger menu) */
        [data-testid="stToolbar"] {
            visibility: hidden !important;
            height: 0px !important;
        }

        /* Hide Streamlit footer */
        footer {
            visibility: hidden !important;
            height: 0px !important;
        }

        footer:after {
            content: "";
            display: none !important;
        }

        /* Remove padding at bottom that appears on mobile */
        .block-container {
            padding-bottom: 0rem !important;
        }
    </style>
"""
st.markdown(clean_ui_css, unsafe_allow_html=True)


# --- Mode Selector ---
mode = st.selectbox("Choose your support style:", ["Therapist", "Friend", "Coach"])

# --- Mood Selector ---
mood = st.radio(
    "How are you feeling right now?",
    ["😊 Happy", "😔 Sad", "😡 Angry", "😨 Anxious", "😐 Neutral"],
    horizontal=True
)
mood_label = mood.split(" ")[1]
st.markdown(f"🧭 Current mood: **{mood}**")

# --- Init Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Message Handler ---
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
        st.session_state["input_text"] = ""  # Clear field

# --- Text Input (Enter to Send) ---
st.text_input("Type your message here...", key="input_text", on_change=handle_message)

# --- Clear Chat Button ---
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.input_text = ""
    st.session_state.clear_chat_triggered = True

# --- Safe rerun if flag is set ---
if st.session_state.get("clear_chat_triggered"):
    st.session_state.clear_chat_triggered = False
    st.experimental_rerun()

# --- Avatar / Role Map ---
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

# --- Display Chat (Latest on Top) ---
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

# --- Safe rerun if clear chat was clicked ---
if st.session_state.get("clear_chat_triggered"):
    st.session_state.clear_chat_triggered = False  # reset flag
    st.experimental_rerun()

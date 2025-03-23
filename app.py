import streamlit as st
from datetime import datetime
from chatbot import get_chatbot_response

# --- Page Config ---
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="centered")
st.title("🧠 Mental Health Support Chatbot")

# --- Hide GitHub icon, footer, and "Hosted with Streamlit" on all devices ---
clean_ui_css = """
    <style>
    /* Hide Streamlit top-right toolbar (GitHub icon, hamburger) */
    [data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0px !important;
    }

    /* Hide standard footer */
    footer {
        visibility: hidden !important;
        height: 0px !important;
    }

    footer:after {
        display: none !important;
    }

    /* Hide "Made with Streamlit" and "Hosted with Streamlit" badge */
    .css-164nlkn.egzxvld1, .css-cio0dv.e1tzin5v2 {
        visibility: hidden !important;
        height: 0px !important;
        display: none !important;
    }

    /* Remove bottom padding on mobile */
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
# --- Sticky Input Box ---
sticky_input_box = """
    <style>
        .sticky-input {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px 15px;
            background-color: #ffffff;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            z-index: 100;
        }

        .sticky-input input {
            width: 100% !important;
            font-size: 16px !important;
        }

        /* Make space so input doesn't cover chat */
        .block-container {
            padding-bottom: 90px !important;
        }
    </style>

    <div class="sticky-input">
"""
st.markdown(sticky_input_box, unsafe_allow_html=True)
st.text_input("Type your message here...", key="input_text", on_change=handle_message, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

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

# --- Custom Footer ---
custom_footer = """
    <div style='text-align: center; padding: 1rem 0; font-size: 14px; color: #888;'>
        Powered by <strong>Grant Thornton</strong> </strong>
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)

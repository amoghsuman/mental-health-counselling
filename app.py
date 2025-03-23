# app.py
import streamlit as st
from chatbot import get_chatbot_response

st.set_page_config(page_title="Mental Health Counseling Chatbot", layout="centered")

st.title("Mental Health Counseling Chatbot")
st.markdown("This chatbot is designed to offer empathetic and thoughtful mental health support.")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("How can I help you today?")

if st.button("Send") and user_input:
    response = get_chatbot_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Chatbot", response))

for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {msg}")

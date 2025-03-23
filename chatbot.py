# chatbot.py
import openai
import streamlit as st

openai.api_key = st.secrets["openai_api_key"]

def get_chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message['content']

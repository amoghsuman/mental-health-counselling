import openai
import streamlit as st
from prompts import get_prompt

client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

def get_chatbot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": get_prompt()},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

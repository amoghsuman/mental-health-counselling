import openai
import streamlit as st
from prompts import get_prompt

# Create OpenAI client (v1.x compatible)
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

def get_chatbot_response(user_input, mode="Therapist"):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": get_prompt(mode)},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

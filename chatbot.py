import openai
import streamlit as st

# Create OpenAI client using the new v1.x syntax
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

def get_chatbot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful, empathetic mental health assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

import openai
import streamlit as st
from prompts import get_prompt

# OpenAI client setup (v1.x compatible)
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

def get_chatbot_response(user_input, mode="Therapist", mood="Neutral"):
    # Build dynamic system prompt
    prompt = get_prompt(mode)
    prompt += f"\n\nThe user is currently feeling {mood.lower()}. Please respond appropriately."

    # Make API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

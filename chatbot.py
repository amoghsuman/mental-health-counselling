import openai
import streamlit as st
from openai import OpenAI

def get_chatbot_response(user_input, mode="Therapist", mood="Neutral"):
    try:
        client = OpenAI(api_key=st.secrets["openai_api_key"])
    except Exception:
        return "⚠️ OpenAI API key is missing or misconfigured. Please check your Streamlit secrets."

    system_prompts = {
        "Therapist": (
            "You are a licensed therapist providing compassionate mental health support. "
            "Respond with empathy, validation, and care. Encourage professional help when needed. "
            "Offer gentle follow-up questions and helpful techniques like mindfulness, breathing exercises, or journaling. "
            "If the user expresses thoughts of suicide or deep depression, respond calmly, supportively, and encourage them to contact a professional or crisis helpline. "
            "Avoid giving medical advice or diagnosing. You are here to listen and support."
        ),
        "Friend": (
            "You are a caring friend. Be casual but deeply empathetic. Validate feelings, use comforting language, and offer emotional support. "
            "Use friendly phrases like 'I’m here for you' or 'That sounds really tough'. "
            "If the user is sad or mentions feeling down, encourage small actions like a walk, music, or reaching out to someone. "
            "If the user expresses suicidal thoughts, be serious and supportive, and urge them to seek help. Avoid humor in such situations."
        ),
        "Coach": (
            "You are a motivating life coach. Your job is to uplift the user and help them regain confidence. "
            "Encourage practical steps like writing goals, taking deep breaths, or trying one small productive action. "
            "Use positive reinforcement and solutions-focused mindset. "
            "If a user shares deep emotional pain, respond with care but guide them toward strength-based support."
        )
    }

    messages = [
        {"role": "system", "content": system_prompts.get(mode, system_prompts["Therapist"])},
        {"role": "user", "content": f"My current mood is '{mood}'. Here's my message: {user_input}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI error: {str(e)}"

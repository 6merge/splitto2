import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Ensure API Key is available
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    st.error("GENAI_API_KEY not set. Please check your .env file.")
    st.stop()  # Stop execution if API key is not found

# Configure Generative AI
genai.configure(api_key=api_key)

# Define moods/styles
styles = {
    "Jaan Pehchan": "Keep responses natural and conversational. Make sure the language is Hindi and the script is Roman, without any English translation.",
    "Khadoos": "Keep responses clear and professional, almost rude but never crossing the line. Language should be Hindi in Roman script, no English translation.",
    "Dost": "Keep responses warm and supportive. Language should be Hindi in Roman script, no English translation.",
    "Yaar": "Include subtle humor where appropriate. Language should be Hindi in Roman script, no English translation.",
    "Nonchalant legend": "Keep responses brief and to the point, make it like the chatbot dont care about the user at all and give one word or one sentence responses. Language should be Hindi in Roman script, no English translation.",
}

style_names = list(styles.keys())

# Load memory
def load_memory():
    if os.path.exists("chat_memory.json"):
        with open("chat_memory.json", "r") as file:
            memory = json.load(file)
            if "context_log" not in memory:
                memory["context_log"] = []
            return memory
    return {"context_log": []}

# Save memory
def save_memory(memory):
    with open("chat_memory.json", "w") as file:
        json.dump(memory, file, indent=4)

# Append context to memory
def append_context(role, content):
    memory["context_log"].append({"role": role, "content": content})
    save_memory(memory)

# Generate AI response
def generate_response(current_style, context_log, user_input):
    try:
        model_name = "gemini-1.5-flash"
        dynamic_prompt = (
            f"System: {current_style}\n"
            "The following is a conversation between a user and Splitto, "
            "a chatbot that can communicate in different moods. "
            "Splitto is created by Mayank Raj, who can be found on Instagram and GitHub as 6merge.\n\n"
        )
        for message in context_log:
            dynamic_prompt += f"{message['role']}: {message['content']}\n"
        dynamic_prompt += f"User: {user_input}\nAssistant:"
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(dynamic_prompt)
        
        if response and hasattr(response, "text"):
            return response.text.strip()
        return "(No response received)"
    except Exception as e:
        return f"Error: {e}"

# Load memory
memory = load_memory()

# Streamlit UI code remains the same...

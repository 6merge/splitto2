import os
import json
import traceback
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Fetch API key
api_key = os.getenv("GOOGLE_API_KEY")

# Ensure API key is available
if not api_key:
    st.error("Google API key is missing. Set GOOGLE_API_KEY in .env file.")
    st.stop()

# Configure Generative AI
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API Configuration Error: {e}")
    st.stop()

# Memory file path
memory_file = "chat_memory.json"

# Define moods/styles with emojis
styles = {
    "😊 Jaan Pehchan": "Conversational and natural Hindi style",
    "😠 Khadoos": "Crisp and slightly irritated tone",
    "🤝 Dost": "Warm and supportive friendly style",
    "😂 Yaar": "Humorous and playful conversation",
    "🙄 Nonchalant": "Minimalist, almost disinterested responses"
}

style_names = list(styles.keys())

# Load memory
def load_memory():
    if os.path.exists(memory_file):
        try:
            with open(memory_file, "r", encoding="utf-8") as file:
                memory = json.load(file)
                memory.setdefault("context_log", [])
                return memory
        except (json.JSONDecodeError, FileNotFoundError):
            return {"context_log": []}
    return {"context_log": []}

# Save memory
def save_memory(memory):
    with open(memory_file, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)

# Generate AI response
def generate_response(current_style, context_log, user_input):
    try:
        # Prepare chat history
        chat_history = [
            {
                'role': 'user',
                'parts': [
                    f"You are Splitto, a mood-based Hindi chatbot. " +
                    f"Current mood: {current_style}. " +
                    "Respond conversationally in Hindi using Roman script."
                ]
            }
        ]

        # Add previous context (adjust context_window as needed)
        context_window = 10
        chat_history.extend(context_log[-context_window:])

        # Generate response
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(user_input)

        return response.text.strip() or "Kuch samajh nahi aaya, phir se bolo"

    except genai.exceptions.RequestError as e:
        # Handle network or API errors
        st.error(f"API Error: {e}")
        return "Is waqt server mein kuch dikkat aa rahi hai. Thodi der mein dubara try karen."
    except genai.exceptions.ModelError as e:
        # Handle model-specific errors (e.g., model unavailability)
        st.error(f"Model Error: {e}")
        return "Iss waqt model uplabdh nahi hai. Thodi der mein dubara try karen."
    except Exception as e:
        # Catch other unexpected errors
        st.error(f"Unexpected Error: {e}")
        return "Maaf karo, kuch gadbad hogayi. Dubara try karen."

# Streamlit UI Configuration
# ... (same as your original code)

# Main App
def main():
    # ... (same as your original code)

if __name__ == "__main__":
    main()
    

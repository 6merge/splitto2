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

        # Add previous context
        for msg in context_log[-5:]:  # Limit context to last 5 messages
            role = 'user' if msg['role'] == 'User' else 'model'
            chat_history.append({
                'role': role, 
                'parts': [msg['content']]
            })

        # Generate response
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(user_input)
        
        return response.text.strip() or "Kuch samajh nahi aaya, phir se bolo"
    
    except Exception as e:
        st.error(f"Response Generation Error: {e}")
        print(traceback.format_exc())
        return "Maaf karo, technical error ho gaya"

# Streamlit UI Configuration
st.set_page_config(
    page_title="Splitto: Mood Chatbot", 
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .chat-container {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 15px;
        max-height: 500px;
        overflow-y: auto;
    }
    .user-message {
        background-color: #4CAF50;
        color: white;
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
        max-width: 80%;
        align-self: flex-end;
    }
    .bot-message {
        background-color: #E3F2FD;
        color: black;
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
        max-width: 80%;
        align-self: flex-start;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #4CAF50;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Main App
def main():
    st.title("🤖 Splitto: Mood-based Chatbot")

    # Memory and session initialization
    memory = load_memory()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Mood Selector
    selected_tone = st.selectbox("Choose Chatbot Mood", style_names)
    current_tone = styles[selected_tone]

    # Chat Display
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            css_class = "user-message" if message["role"] == "User" else "bot-message"
            st.markdown(f'<div class="{css_class}">{message["content"]}</div>', unsafe_allow_html=True)

    # Chat Input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Type your message", 
            key="chat_input", 
            placeholder="Apna sawal poochho..."
        )
    
    with col2:
        send_button = st.button("Send")

    # Message Handling
    if (user_input and send_button) or (user_input and st.session_state.get('last_input') != user_input):
        st.session_state['last_input'] = user_input
        
        # User Message
        st.session_state.chat_history.append({
            "role": "User", 
            "content": user_input
        })
        memory["context_log"].append({
            "role": "User", 
            "content": user_input
        })

        # Bot Response
        bot_response = generate_response(current_tone, memory["context_log"], user_input)
        st.session_state.chat_history.append({
            "role": "Assistant", 
            "content": bot_response
        })
        memory["context_log"].append({
            "role": "Assistant", 
            "content": bot_response
        })

        # Save memory and rerun
        save_memory(memory)
        st.experimental_rerun()

    # Footer
    st.markdown("---")
    st.markdown("🌟 Created by Mayank Raj | [GitHub](https://github.com/6merge)")

if __name__ == "__main__":
    main()

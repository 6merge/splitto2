import os
import json
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Fetch API key
api_key = os.getenv("GOOGLE_API_KEY")

# Ensure API key is available
if not api_key:
    st.error("Google Generative AI API key is missing. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Configure Generative AI
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring Generative AI: {e}")
    st.stop()

# Memory file path
memory_file = "chat_memory.json"

# Define moods/styles
styles = {
    "Jaan Pehchan": "Keep responses natural and conversational. Make sure the language is Hindi and the script is Roman, without any English translation.",
    "Khadoos": "Keep responses clear and professional, almost rude but never crossing the line. Language should be Hindi in Roman script, no English translation.",
    "Dost": "Keep responses warm and supportive. Language should be Hindi in Roman script, no English translation.",
    "Yaar": "Include subtle humor where appropriate. Language should be Hindi in Roman script, no English translation.",
    "Nonchalant legend": "Keep responses brief and to the point, make it like the chatbot doesn't care about the user at all and give one word or one sentence responses. Language should be Hindi in Roman script, no English translation.",
}

style_names = list(styles.keys())

# Load memory
def load_memory():
    if os.path.exists(memory_file):
        try:
            with open(memory_file, "r", encoding="utf-8") as file:
                memory = json.load(file)
                if "context_log" not in memory:
                    memory["context_log"] = []
                return memory
        except json.JSONDecodeError:
            return {"context_log": []}
    return {"context_log": []}

# Save memory
def save_memory(memory):
    with open(memory_file, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)

# Append context to memory
def append_context(memory, role, content):
    memory["context_log"].append({"role": role, "content": content})
    save_memory(memory)

# Generate AI response
def generate_response(current_style, context_log, user_input):
    try:
        # Prepare dynamic prompt
        dynamic_prompt = (
            f"System: {current_style}\n"
            "The following is a conversation between a user and Splitto, "
            "a chatbot that can communicate in different moods. "
            "Splitto is created by Mayank Raj, who can be found on Instagram and GitHub as 6merge.\n\n"
        )
        for message in context_log:
            dynamic_prompt += f"{message['role']}: {message['content']}\n"
        dynamic_prompt += f"User: {user_input}\nAssistant:"

        # Use Gemini Flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(dynamic_prompt, 
                                          generation_config=genai.types.GenerationConfig(
                                              temperature=0.7,
                                              max_output_tokens=100
                                          ))
        
        return response.text.strip()
    
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "(Kuch gadbad ho gayi, phir se try karo)"

# Streamlit UI Configuration
st.set_page_config(page_title="Splitto - Mood-based Hindi Chatbot", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        text-align: center;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
    }
    .user-bubble {
        background-color: #4caf50;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .bot-bubble {
        background-color: #e3f2fd;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Main App
def main():
    st.title("🤖 Splitto: Mood-based Hindi Chatbot")

    # Load memory
    memory = load_memory()

    # Tone Selector
    selected_tone = st.selectbox("Choose Chatbot Mood", style_names)
    current_tone = styles[selected_tone]

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    with st.container():
        for message in st.session_state.chat_history:
            css_class = "user-bubble" if message["role"] == "User" else "bot-bubble"
            st.markdown(f'<div class="{css_class}">{message["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    user_input = st.text_input("Type your message:", key="user_input", placeholder="Apna sawal poochho...")

    if user_input and st.button("Send"):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "User", "content": user_input})
        append_context(memory, "User", user_input)

        # Generate bot response
        bot_response = generate_response(current_tone, memory["context_log"], user_input)
        st.session_state.chat_history.append({"role": "Assistant", "content": bot_response})
        append_context(memory, "Assistant", bot_response)

        # Rerun to refresh the page and show new messages
        st.experimental_rerun()

    # Footer
    st.markdown("---")
    st.markdown("🌟 Created by **Mayank Raj**. Connect on [GitHub](https://github.com/6merge) and [Instagram](https://www.instagram.com/6merge).")

if __name__ == "__main__":
    main()
    

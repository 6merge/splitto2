from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # This allows cross-origin requests

# Load API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set GENAI_API_KEY in the .env file.")

# Configure Generative AI
genai.configure(api_key=api_key)
model_name = "gemini-1.5-flash"

# Function to check if the message is asking about the bot
def is_about_bot(user_input):
    about_bot_keywords = ["who are you", "what are you", "tell me about yourself", "who is splitto", "introduce yourself"]
    return any(keyword in user_input.lower() for keyword in about_bot_keywords)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    style = data.get("style", "casual")
    messages = data.get("messages", [])
    user_input = data.get("userInput", "")

    # Check if the user is asking about the bot's identity
    if is_about_bot(user_input):
        response_text = ("Hi, I'm Splitto! I'm a multiple personality chatbot created by Mayank Raj Singh. "
                         "You can find me on GitHub and Instagram as @6merge. How can I assist you today?")
        return jsonify({"response": response_text})

    # Build context and prompt for regular conversation
    context = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    prompt = f"System: {style}\n{context}\nUser: {user_input}\nAssistant:"

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return jsonify({"response": response.text.strip()})
    except Exception as e:
        print(f"Error generating response: {str(e)}")  # Log error on server for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)

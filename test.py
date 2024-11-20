import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Generative AI model with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Test API call
try:
    model_name = "gemini-1.5-flash"
    prompt = "Hello! How are you?"
    response = genai.generate_text(
        model=model_name,
        prompt=prompt
    )
    print(response)
except Exception as e:
    print(f"Error: {e}")

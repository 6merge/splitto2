require('dotenv').config();  // Load environment variables from .env file

const GOOGLE_API_KEY = process.env.GOOGLE_API_KEY; // Get the API key from the .env file

if (!GOOGLE_API_KEY) {
    console.error("API key is missing! Please set GOOGLE_API_KEY in your .env file.");
    process.exit(1);  // Exit if the API key is not found
}

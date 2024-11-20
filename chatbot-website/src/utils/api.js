import axios from "axios";

const API_URL = "http://localhost:5000/chat";  // Replace with your backend URL


// Function to fetch the chatbot's response
export const fetchResponse = async (style, messages, userInput) => {
    try {
      const response = await axios.post(API_URL, {
        style,
        messages,
        userInput
      });
      return { role: "Assistant", content: response.data.response };
    } catch (error) {
      console.error("Error fetching response:", error); // Log any error to the console for debugging
      return { role: "Assistant", content: "Error fetching response." };
    }
  };


export const saveMemory = (memory) => {
  localStorage.setItem("chatMemory", JSON.stringify(memory));
};

export const loadMemory = () => {
  const memory = localStorage.getItem("chatMemory");
  return memory ? JSON.parse(memory) : [];
};

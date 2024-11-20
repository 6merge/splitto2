import React, { useState, useEffect } from "react";
import Message from "./Message";
import { fetchResponse, saveMemory, loadMemory } from "../utils/api";
import "../styles/ChatBox.css"; 

const ChatBox = () => {
  const [messages, setMessages] = useState([]);  // Start with an empty message state
  const [input, setInput] = useState("");
  const [style, setStyle] = useState("casual");

  // Load messages from localStorage for training, but don't show them
  useEffect(() => {
    const memory = loadMemory();
    // Store the memory for training, but do not display it
    saveMemory(memory);  // Store messages for training
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return; // Don't send if input is empty

    const userMessage = { role: "User", content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Clear the input field immediately after sending the message
    setInput("");

    const assistantResponse = await fetchResponse(style, messages, input);
    const newMessages = [...messages, userMessage, assistantResponse];

    setMessages(newMessages);
    saveMemory(newMessages);  // Store the new messages for future training
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevent default Enter behavior (form submission)
      handleSend();
    }
  };

  useEffect(() => {
    // Save memory after each new message is sent
    saveMemory(messages);
  }, [messages]);

  return (
    <div className={`chat-container ${style}`}>
      <div className="message-container">
        {messages.map((msg, idx) => (
          <Message key={idx} role={msg.role} content={msg.content} />
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown} // Trigger on key press
        placeholder="Type a message..."
      />
      <button onClick={handleSend}>Send</button>
      <select onChange={(e) => setStyle(e.target.value)} value={style}>
        <option value="casual">Casual</option>
        <option value="formal">Formal</option>
        <option value="friendly">Friendly</option>
        <option value="witty">Witty</option>
        <option value="direct">Direct</option>
      </select>
    </div>
  );
};

export default ChatBox;

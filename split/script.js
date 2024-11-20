// config.js
require('dotenv').config();  // Load environment variables from .env file

const GOOGLE_API_KEY = process.env.GOOGLE_API_KEY; // Get the API key from the .env file

if (!GOOGLE_API_KEY) {
    console.error("API key is missing! Please set GOOGLE_API_KEY in your .env file.");
    process.exit(1);  // Exit if the API key is not found
}

// chatbot.js
class SplitChatbot {
    constructor() {
        this.personalities = {
            mayank: {
                style: "casual",
                prompt: "Keep responses casual and natural. Use everyday language. Be relaxed and conversational.",
                greeting: "Hey! What's up? I'm Mayank. Let's chat!",
                traits: "Casual & Laid-back"
            },
            kaveri: {
                style: "formal",
                prompt: "Maintain professional and structured communication. Use precise language. Be clear and concise.",
                greeting: "Greetings, I'm Kaveri. How may I assist you today?",
                traits: "Formal & Professional"
            },
            mamrit: {
                style: "friendly",
                prompt: "Be warm, friendly, and supportive. Show enthusiasm and positivity. Make the user feel comfortable.",
                greeting: "Hi there! I'm Mamrit, and I'm really happy to chat with you!",
                traits: "Friendly & Supportive"
            },
            gauri: {
                style: "witty",
                prompt: "Be witty and clever while staying helpful. Include subtle humor where appropriate.",
                greeting: "Hello! Gauri here, ready to chat with a dash of wit!",
                traits: "Witty & Humorous"
            },
            raj: {
                style: "direct",
                prompt: "Be direct, clear, and straightforward. Get straight to the point. Provide concise responses.",
                greeting: "Hi, I'm Raj. How can I help?",
                traits: "Direct & Straightforward"
            }
        };

        this.currentPersonality = null;
        this.messageHistory = new Map(); // Store chat history for each personality
        this.initializeUI();
    }

    initializeUI() {
        // Add personality cards to the grid
        const grid = document.querySelector('.personality-grid');
        grid.innerHTML = ''; // Clear existing cards

        Object.entries(this.personalities).forEach(([name, data]) => {
            const card = this.createPersonalityCard(name, data);
            grid.appendChild(card);
        });

        // Initialize event listeners
        this.initializeEventListeners();
    }

    createPersonalityCard(name, data) {
        const card = document.createElement('div');
        card.className = 'personality-card';
        card.innerHTML = `
            <div class="avatar">${name[0].toUpperCase()}</div>
            <h2 class="personality-name">${name.charAt(0).toUpperCase() + name.slice(1)}</h2>
            <p class="personality-trait">${data.traits}</p>
            <button class="chat-btn">Chat with ${name.charAt(0).toUpperCase() + name.slice(1)}</button>
        `;
        card.onclick = () => this.openChat(name);
        return card;
    }

    initializeEventListeners() {
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.querySelector('.send-btn');

        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        sendButton.addEventListener('click', () => this.sendMessage());

        // Close chat button
        document.querySelector('.close-chat').addEventListener('click', () => this.closeChat());
    }

    async openChat(personalityName) {
        this.currentPersonality = personalityName.toLowerCase();
        const personality = this.personalities[this.currentPersonality];

        const chatModal = document.getElementById('chatModal');
        const chatMessages = document.getElementById('chatMessages');
        const chatName = document.getElementById('chatName');

        chatModal.style.display = 'block';
        chatName.textContent = `Chatting with ${personalityName.charAt(0).toUpperCase() + personalityName.slice(1)}`;

        // Load or initialize chat history
        if (!this.messageHistory.has(this.currentPersonality)) {
            this.messageHistory.set(this.currentPersonality, []);
            this.addMessageToChat('bot', personality.greeting);
        } else {
            chatMessages.innerHTML = '';
            this.messageHistory.get(this.currentPersonality).forEach(msg => {
                this.addMessageToChat(msg.sender, msg.content);
            });
        }
    }

    closeChat() {
        document.getElementById('chatModal').style.display = 'none';
        document.getElementById('messageInput').value = '';
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();

        if (!message || !this.currentPersonality) return;

        // Add user message
        this.addMessageToChat('user', message);
        this.saveMessage('user', message);
        messageInput.value = '';

        // Show typing indicator
        const typingIndicator = this.addTypingIndicator();

        try {
            const response = await this.generateResponse(message);
            typingIndicator.remove();
            this.addMessageToChat('bot', response);
            this.saveMessage('bot', response);
        } catch (error) {
            typingIndicator.remove();
            const errorMessage = 'Sorry, I encountered an error processing your message.';
            this.addMessageToChat('bot', errorMessage);
            this.saveMessage('bot', errorMessage);
        }
    }

    async generateResponse(message) {
        try {
            const personality = this.personalities[this.currentPersonality];
            const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${GOOGLE_API_KEY}`
                },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: `${personality.prompt}\n\nUser: ${message}\nAssistant: `
                        }]
                    }]
                })
            });

            const data = await response.json();
            if (data.candidates && data.candidates[0]?.content?.parts[0]?.text) {
                return data.candidates[0].content.parts[0].text;
            } else {
                throw new Error('Invalid response format');
            }
        } catch (error) {
            console.error('Error generating response:', error);
            throw error;
        }
    }

    addMessageToChat(sender, message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `
            <div class="message-bubble ${sender === 'user' ? 'user-bubble' : 'bot-bubble'}">
                ${message}
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    addTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const indicator = document.createElement('div');
        indicator.className = 'message bot-message typing-indicator';
        indicator.innerHTML = `
            <div class="message-bubble bot-bubble">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        `;
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return indicator;
    }

    saveMessage(sender, content) {
        const history = this.messageHistory.get(this.currentPersonality);
        history.push({ sender, content });
        this.messageHistory.set(this.currentPersonality, history);
    }
}

// Initialize the chatbot when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new SplitChatbot();
});

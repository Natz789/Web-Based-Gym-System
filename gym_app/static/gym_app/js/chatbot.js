/**
 * Intelligent Chatbot Widget
 * Gym Management System
 */

class GymChatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.init();
    }

    init() {
        // Create chatbot HTML
        this.createChatWidget();
        // Attach event listeners
        this.attachEventListeners();
        // Load chat history from localStorage
        this.loadChatHistory();
        // Send welcome message
        this.sendWelcomeMessage();
    }

    createChatWidget() {
        const chatHTML = `
            <!-- Chatbot Toggle Button -->
            <div id="chatbot-toggle" class="chatbot-toggle">
                <i class="fas fa-comments"></i>
                <span class="chatbot-badge" id="chatbot-badge">1</span>
            </div>

            <!-- Chatbot Window -->
            <div id="chatbot-window" class="chatbot-window">
                <div class="chatbot-header">
                    <div class="chatbot-header-content">
                        <i class="fas fa-robot"></i>
                        <div>
                            <h4>Gym Assistant</h4>
                            <span class="chatbot-status">Online</span>
                        </div>
                    </div>
                    <div class="chatbot-actions">
                        <button id="chatbot-minimize" class="chatbot-btn-icon" title="Minimize">
                            <i class="fas fa-minus"></i>
                        </button>
                        <button id="chatbot-clear" class="chatbot-btn-icon" title="Clear Chat">
                            <i class="fas fa-trash"></i>
                        </button>
                        <button id="chatbot-close" class="chatbot-btn-icon" title="Close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>

                <div class="chatbot-messages" id="chatbot-messages">
                    <!-- Messages will be dynamically added here -->
                </div>

                <div class="chatbot-input-container">
                    <div class="chatbot-quick-replies" id="chatbot-quick-replies">
                        <button class="quick-reply-btn" data-message="Show membership plans">💪 Plans</button>
                        <button class="quick-reply-btn" data-message="What payment methods do you accept?">💳 Payment</button>
                        <button class="quick-reply-btn" data-message="My membership status">📊 Status</button>
                        <button class="quick-reply-btn" data-message="help">❓ Help</button>
                    </div>
                    <div class="chatbot-input-wrapper">
                        <input
                            type="text"
                            id="chatbot-input"
                            class="chatbot-input"
                            placeholder="Type your message..."
                            autocomplete="off"
                        />
                        <button id="chatbot-send" class="chatbot-send-btn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                    <div class="chatbot-typing" id="chatbot-typing" style="display: none;">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `;

        // Append to body
        document.body.insertAdjacentHTML('beforeend', chatHTML);
    }

    attachEventListeners() {
        // Toggle button
        document.getElementById('chatbot-toggle').addEventListener('click', () => {
            this.toggleChat();
        });

        // Close button
        document.getElementById('chatbot-close').addEventListener('click', () => {
            this.closeChat();
        });

        // Minimize button
        document.getElementById('chatbot-minimize').addEventListener('click', () => {
            this.closeChat();
        });

        // Clear button
        document.getElementById('chatbot-clear').addEventListener('click', () => {
            this.clearChat();
        });

        // Send button
        document.getElementById('chatbot-send').addEventListener('click', () => {
            this.sendMessage();
        });

        // Enter key to send
        document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Quick reply buttons
        document.querySelectorAll('.quick-reply-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const message = e.target.getAttribute('data-message');
                this.sendQuickReply(message);
            });
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chatbot-window');
        const chatToggle = document.getElementById('chatbot-toggle');
        const badge = document.getElementById('chatbot-badge');

        if (this.isOpen) {
            chatWindow.classList.add('open');
            chatToggle.classList.add('active');
            badge.style.display = 'none';
            this.scrollToBottom();
        } else {
            chatWindow.classList.remove('open');
            chatToggle.classList.remove('active');
        }
    }

    openChat() {
        if (!this.isOpen) {
            this.toggleChat();
        }
    }

    closeChat() {
        if (this.isOpen) {
            this.toggleChat();
        }
    }

    sendWelcomeMessage() {
        if (this.messages.length === 0) {
            const welcomeMsg = "👋 Hello! I'm your Gym Assistant. I can help you with:\n\n" +
                "• Membership plans and pricing\n" +
                "• Walk-in passes\n" +
                "• Payment methods\n" +
                "• Your membership status\n" +
                "• And more!\n\n" +
                "How can I assist you today?";
            this.addMessage(welcomeMsg, 'bot');
        }
    }

    sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();

        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        this.showTyping();

        // Send to backend
        this.sendToBackend(message);
    }

    sendQuickReply(message) {
        // Add user message
        this.addMessage(message, 'user');

        // Show typing indicator
        this.showTyping();

        // Send to backend
        this.sendToBackend(message);
    }

    async sendToBackend(message) {
        try {
            const response = await fetch('/api/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Hide typing indicator
            this.hideTyping();

            if (response.ok) {
                // Add bot response
                this.addMessage(data.response, 'bot');
            } else {
                // Show error message
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Chatbot error:', error);
            this.hideTyping();
            this.addMessage('Sorry, I\'m having trouble connecting. Please try again later.', 'bot');
        }
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}-message`;

        const time = new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });

        // Format message text (preserve line breaks)
        const formattedText = text.replace(/\n/g, '<br>');

        messageDiv.innerHTML = `
            <div class="message-content">
                ${sender === 'bot' ? '<i class="fas fa-robot message-icon"></i>' : ''}
                <div class="message-text">${formattedText}</div>
            </div>
            <div class="message-time">${time}</div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();

        // Save to messages array
        this.messages.push({ text, sender, time });
        this.saveChatHistory();
    }

    showTyping() {
        document.getElementById('chatbot-typing').style.display = 'flex';
        this.scrollToBottom();
    }

    hideTyping() {
        document.getElementById('chatbot-typing').style.display = 'none';
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chatbot-messages');
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }

    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.messages = [];
            document.getElementById('chatbot-messages').innerHTML = '';
            localStorage.removeItem('gym_chatbot_history');
            this.sendWelcomeMessage();
        }
    }

    saveChatHistory() {
        try {
            // Save only last 50 messages
            const recentMessages = this.messages.slice(-50);
            localStorage.setItem('gym_chatbot_history', JSON.stringify(recentMessages));
        } catch (e) {
            console.error('Failed to save chat history:', e);
        }
    }

    loadChatHistory() {
        try {
            const saved = localStorage.getItem('gym_chatbot_history');
            if (saved) {
                this.messages = JSON.parse(saved);
                // Restore messages to UI
                const messagesContainer = document.getElementById('chatbot-messages');
                this.messages.forEach(msg => {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `chatbot-message ${msg.sender}-message`;
                    const formattedText = msg.text.replace(/\n/g, '<br>');
                    messageDiv.innerHTML = `
                        <div class="message-content">
                            ${msg.sender === 'bot' ? '<i class="fas fa-robot message-icon"></i>' : ''}
                            <div class="message-text">${formattedText}</div>
                        </div>
                        <div class="message-time">${msg.time}</div>
                    `;
                    messagesContainer.appendChild(messageDiv);
                });
            }
        } catch (e) {
            console.error('Failed to load chat history:', e);
        }
    }
}

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.gymChatbot = new GymChatbot();
});

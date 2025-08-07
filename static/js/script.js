document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const aiModeButton = document.getElementById('aiModeButton');
    const pythonModeButton = document.getElementById('pythonModeButton');
    const currentModeSpan = document.getElementById('currentMode');
    let currentMode = 'AI';

    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `d-flex mb-2 ${isUser ? 'user-message' : 'bot-message'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dots">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        `;
        typingDiv.id = 'typingIndicator';
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    function updateMode(mode) {
        currentMode = mode;
        currentModeSpan.textContent = mode;
        aiModeButton.classList.toggle('active', mode === 'AI');
        pythonModeButton.classList.toggle('active', mode === 'Python');
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        addMessage(message, true);
        userInput.value = '';
        sendButton.disabled = true;
        showTypingIndicator();
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message, mode: currentMode })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (!data.response || data.response.trim() === '') {
                throw new Error('Empty response from server');
            }
            
            removeTypingIndicator();
            addMessage(data.response, false);
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage(`Error: ${error.message}`, false);
        } finally {
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    aiModeButton.addEventListener('click', () => updateMode('AI'));
    pythonModeButton.addEventListener('click', () => updateMode('Python'));
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
});
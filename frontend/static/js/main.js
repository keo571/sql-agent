// frontend/static/js/main.js
function addMessageToChat(role, message) {
    const chatHistory = document.getElementById('chatHistory');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;

    // Split the message into SQL Query and Result sections
    const sections = message.split('\n\n');

    sections.forEach(section => {
        if (section.trim()) {
            const sectionDiv = document.createElement('div');
            sectionDiv.className = 'message-section';

            // Create a pre element to preserve whitespace and formatting
            const preElement = document.createElement('pre');
            preElement.textContent = section;
            sectionDiv.appendChild(preElement);

            messageDiv.appendChild(sectionDiv);
        }
    });

    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessageToChat('user', message);
    userInput.value = '';

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message })
        });

        const data = await response.json();

        // Add AI response to chat
        addMessageToChat('ai', data.response);

    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('ai', 'Sorry, there was an error processing your request.');
    }
}

// Handle Enter key
document.getElementById('userInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
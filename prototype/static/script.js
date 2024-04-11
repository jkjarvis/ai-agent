const chatDiv = document.getElementById('chat');

function fetchMessages() {
    fetch('/get-messages')
        .then(response => response.json())
        .then(data => {
            chatDiv.innerHTML = ''; // Clear current chat
            data.messages.forEach(message => {
                for (const [sender, text] of Object.entries(message)) {
                    displayMessage(text, sender); // Display message
                }
            });
        })
        .catch(error => console.error('Error fetching messages:', error));
}

function sendMessage(message) {
    fetch('/send-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(message),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Message sent:', data);
        fetchMessages(); // Refresh messages after sending
    })
    .catch((error) => {
        console.error('Error sending message:', error);
    });
}

function displayMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender.replace(/\s+/g, '-').toLowerCase()); // Convert sender to CSS class
    messageDiv.textContent = `${sender}: ${message}`;
    chatDiv.appendChild(messageDiv);
}

// Example usage
// sendMessage({"user": "Hi there!"});
// sendMessage({"customer executive": "Hello, how can I help you?"});

// Fetch messages every 5 seconds
setInterval(fetchMessages, 5000);

// Initial fetch
fetchMessages();

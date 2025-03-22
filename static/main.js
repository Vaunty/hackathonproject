
// Dummy transit data
const transitRecommendations = [
    "Bus Route 42 arriving in 5 minutes at Market Street",
    "Express Train to Downtown departing in 10 minutes",
    "Bike sharing station has 5 bikes available nearby"
];

// Update transit recommendations
function updateTransit() {
    const transitDiv = document.getElementById('transit-results');
    transitDiv.innerHTML = transitRecommendations.map(rec => `<p>${rec}</p>`).join('');
}

// Chat functionality
function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value;
    if (message.trim() === '') return;

    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML += `<p><strong>You:</strong> ${message}</p>`;

    // Send to backend and get response
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chatMessages.innerHTML += `<p><strong>AI:</strong> ${data.response}</p>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    input.value = '';
}

// Vision detection
function detectObjects() {
    const results = document.getElementById('detection-results');
    results.innerHTML = 'Analyzing street view...';
    fetch('/detect', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const results = document.getElementById('detection-results');
        results.innerHTML = `<h3>Detected Objects:</h3>
            <ul>${data.objects.map(obj => `<li>${obj}</li>`).join('')}</ul>`;
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateTransit();
    detectObjects();
    
    // Update transit info every 30 seconds
    setInterval(updateTransit, 30000);
});

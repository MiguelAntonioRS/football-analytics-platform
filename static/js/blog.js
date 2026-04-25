let chatMessages = [];

async function loadChatMessages() {
    try {
        const response = await fetch('/api/blog/chat/');
        const data = await response.json();
        chatMessages = data.reverse();
        renderChatMessages();
    } catch (error) {
        console.error('Error loading chat:', error);
    }
}

function renderChatMessages() {
    const container = document.getElementById('chatMessages');
    if (!container) return;
    container.innerHTML = '';

    chatMessages.slice(-20).forEach(msg => {
        const div = document.createElement('div');
        div.className = 'mb-2 p-2 bg-light rounded';
        div.innerHTML = `
            <strong>${msg.username}</strong>
            <span class="text-muted small ms-2">${new Date(msg.created_at).toLocaleTimeString()}</span>
            <p class="mb-0">${msg.content}</p>
        `;
        container.appendChild(div);
    });

    container.scrollTop = container.scrollHeight;
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const content = input.value.trim();

    if (!content) return;

    try {
        const token = localStorage.getItem('token');
        if (!token) {
            alert('Inicia sesión para chatear');
            return;
        }

        const response = await fetch('/api/blog/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ content })
        });

        if (response.ok) {
            input.value = '';
            loadChatMessages();
        }
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

document.getElementById('chatInput')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendChatMessage();
    }
});

document.addEventListener('DOMContentLoaded', loadChatMessages);
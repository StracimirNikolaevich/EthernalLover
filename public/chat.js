// Chat functionality for character conversations

let currentCharacterId = null;

// Initialize chat for a character
async function initChat(characterId) {
    currentCharacterId = characterId;
    await loadChatHistory(characterId);
    setupChatInput(characterId);
}

// Load chat history
async function loadChatHistory(characterId) {
    try {
        const headers = await window.getAuthHeaders();
        const response = await fetch(`/api/messages?character_id=${characterId}`, { headers });
        const data = await response.json();
        
        if (data.success && data.messages) {
            displayMessages(data.messages);
        } else {
            console.error('Error loading chat history:', data.error);
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Display messages in chat
function displayMessages(messages) {
    const container = document.getElementById('chatMessages');
    if (!container) return;
    
    if (messages.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: #999; padding: 20px;">No messages yet. Start the conversation!</div>';
        return;
    }
    
    container.innerHTML = messages.map(msg => createMessageElement(msg)).join('');
    scrollToBottom();
}

// Create message element
function createMessageElement(message) {
    const isUser = message.sender_type === 'user';
    const timestamp = new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const avatar = isUser ? 'You' : (message.character_name || 'AI');
    const avatarInitial = avatar.charAt(0).toUpperCase();
    
    let imageHtml = '';
    if (message.image_url) {
        imageHtml = `<img src="${escapeHtml(message.image_url)}" alt="Image" class="message-image" onerror="this.style.display='none'">`;
    }
    
    return `
        <div class="message ${isUser ? 'user' : ''}">
            <div class="message-avatar">${avatarInitial}</div>
            <div class="message-content">
                ${message.message_text ? `<div class="message-text">${escapeHtml(message.message_text)}</div>` : ''}
                ${imageHtml}
                <div class="message-time">${timestamp}</div>
            </div>
        </div>
    `;
}

// Setup chat input handlers
function setupChatInput(characterId) {
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const imageBtn = document.getElementById('imageUploadBtn');
    const fileInput = document.getElementById('imageFileInput');
    
    if (!input || !sendBtn) return;
    
    // Send on Enter key
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(characterId);
        }
    });
    
    // Send button click
    sendBtn.addEventListener('click', () => {
        sendMessage(characterId);
    });
    
    // Image upload
    if (imageBtn && fileInput) {
        imageBtn.addEventListener('click', () => {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (file) {
                await uploadAndSendImage(characterId, file);
                fileInput.value = ''; // Reset input
            }
        });
    }
}

// Send text message
async function sendMessage(characterId) {
    const input = document.getElementById('chatInput');
    if (!input) return;
    
    const text = input.value.trim();
    if (!text) return;
    
    // Disable input while sending
    input.disabled = true;
    const sendBtn = document.getElementById('sendBtn');
    if (sendBtn) sendBtn.disabled = true;
    
    try {
        const headers = await window.getAuthHeaders();
        const response = await fetch('/api/messages', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                character_id: characterId,
                message_text: text,
                sender_type: 'user'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            input.value = '';
            // Reload chat history to show new message
            await loadChatHistory(characterId);
        } else {
            alert('Error sending message: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Error sending message. Please try again.');
    } finally {
        input.disabled = false;
        if (sendBtn) sendBtn.disabled = false;
        input.focus();
    }
}

// Upload and send image
async function uploadAndSendImage(characterId, file) {
    // Validate file
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file.');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
        alert('Image size must be less than 5MB.');
        return;
    }
    
    const sendBtn = document.getElementById('sendBtn');
    if (sendBtn) sendBtn.disabled = true;
    
    try {
        // Upload image
        const formData = new FormData();
        formData.append('image', file);
        formData.append('character_id', characterId);
        
        const headers = await window.getAuthHeaders();
        delete headers['Content-Type']; // Let browser set it for FormData
        
        const uploadResponse = await fetch('/api/upload', {
            method: 'POST',
            headers: headers,
            body: formData
        });
        
        const uploadData = await uploadResponse.json();
        
        if (!uploadData.success || !uploadData.image_url) {
            throw new Error(uploadData.error || 'Failed to upload image');
        }
        
        // Send message with image
        const messageHeaders = await window.getAuthHeaders();
        const messageResponse = await fetch('/api/messages', {
            method: 'POST',
            headers: messageHeaders,
            body: JSON.stringify({
                character_id: characterId,
                image_url: uploadData.image_url,
                sender_type: 'user'
            })
        });
        
        const messageData = await messageResponse.json();
        
        if (messageData.success) {
            await loadChatHistory(characterId);
        } else {
            throw new Error(messageData.error || 'Failed to send image');
        }
    } catch (error) {
        console.error('Error uploading image:', error);
        alert('Error uploading image: ' + error.message);
    } finally {
        if (sendBtn) sendBtn.disabled = false;
    }
}

// Scroll chat to bottom
function scrollToBottom() {
    const container = document.getElementById('chatMessages');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// Format timestamp
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) { // Less than 1 minute
        return 'Just now';
    } else if (diff < 3600000) { // Less than 1 hour
        return Math.floor(diff / 60000) + ' minutes ago';
    } else if (diff < 86400000) { // Less than 1 day
        return Math.floor(diff / 3600000) + ' hours ago';
    } else {
        return date.toLocaleDateString();
    }
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export functions
window.initChat = initChat;
window.loadChatHistory = loadChatHistory;
window.sendMessage = sendMessage;
window.uploadAndSendImage = uploadAndSendImage;

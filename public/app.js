// Navigation and character management functions

// Get auth token for API requests
async function getAuthHeaders() {
    const session = await window.supabaseAuth.getSession();
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (session?.access_token) {
        headers['Authorization'] = `Bearer ${session.access_token}`;
    }
    
    return headers;
}

// Navigate to a page
function navigateTo(page) {
    window.location.href = page;
}

// Load all characters for the user
async function loadCharacters() {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch('/api/characters', { headers });
        const data = await response.json();
        
        if (data.success && data.characters) {
            return data.characters;
        } else {
            console.error('Error loading characters:', data.error);
            return [];
        }
    } catch (error) {
        console.error('Error loading characters:', error);
        return [];
    }
}

// Load a single character by ID
async function loadCharacter(characterId) {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`/api/character?id=${characterId}`, { headers });
        const data = await response.json();
        
        if (data.success && data.character) {
            return data.character;
        } else {
            console.error('Error loading character:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Error loading character:', error);
        return null;
    }
}

// Create a new character
async function createCharacter(preferences) {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ preferences })
        });
        
        const data = await response.json();
        
        if (data.success && data.character) {
            return data.character;
        } else {
            throw new Error(data.error || 'Failed to create character');
        }
    } catch (error) {
        console.error('Error creating character:', error);
        throw error;
    }
}

// Delete a character
async function deleteCharacter(characterId) {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`/api/character?id=${characterId}`, {
            method: 'DELETE',
            headers: headers
        });
        
        const data = await response.json();
        return data.success;
    } catch (error) {
        console.error('Error deleting character:', error);
        return false;
    }
}

// Display characters in grid
function displayCharacters(characters, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (characters.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No characters yet. Create your first AI companion!</p>';
        return;
    }
    
    const createCard = `
        <div class="character-card create-character-card" onclick="showCreateCharacterModal()">
            <div class="icon">+</div>
            <h3>Create New Character</h3>
        </div>
    `;
    
    const characterCards = characters.map(char => `
        <div class="character-card" onclick="navigateTo('/character?id=${char.id}')">
            <h3>${escapeHtml(char.name || 'Unnamed')}</h3>
            <p><strong>Personality:</strong> ${escapeHtml(char.personality || 'Not set')}</p>
            <p><strong>Interests:</strong> ${escapeHtml(char.interests || 'Not set')}</p>
        </div>
    `).join('');
    
    container.innerHTML = createCard + characterCards;
}

// Display character details
function displayCharacterDetails(character, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
        <div class="character-detail">
            <h2>${escapeHtml(character.name || 'Unnamed Character')}</h2>
            <div class="info-section">
                <div class="info-label">Personality</div>
                <div class="info-value">${escapeHtml(character.personality || 'Not set')}</div>
            </div>
            <div class="info-section">
                <div class="info-label">Appearance</div>
                <div class="info-value">${escapeHtml(character.appearance || 'Not set')}</div>
            </div>
            <div class="info-section">
                <div class="info-label">Interests</div>
                <div class="info-value">${escapeHtml(character.interests || 'Not set')}</div>
            </div>
            <div class="info-section">
                <div class="info-label">Age</div>
                <div class="info-value">${escapeHtml(character.age || 'Not set')}</div>
            </div>
            <div class="info-section">
                <div class="info-label">Backstory</div>
                <div class="info-value">${escapeHtml(character.backstory || 'Not set')}</div>
            </div>
            <div class="action-buttons">
                <button class="btn btn-secondary" onclick="navigateTo('/characters')">Back to Characters</button>
                <button class="btn btn-danger" onclick="deleteCurrentCharacter()">Delete Character</button>
            </div>
        </div>
    `;
}

// Show create character modal
function showCreateCharacterModal() {
    const name = prompt('Enter character name (optional):');
    if (name === null) return; // User cancelled
    
    const personality = prompt('Enter personality traits:', 'sweet and caring');
    if (personality === null) return;
    
    const appearance = prompt('Enter appearance description:', 'beautiful with a warm smile');
    if (appearance === null) return;
    
    const interests = prompt('Enter interests:', 'reading, music, art');
    if (interests === null) return;
    
    const age = prompt('Enter age range:', '20s');
    if (age === null) return;
    
    createCharacterWithPreferences({
        name: name.trim() || undefined,
        personality: personality.trim(),
        appearance: appearance.trim(),
        interests: interests.trim(),
        age: age.trim()
    });
}

// Create character with preferences
async function createCharacterWithPreferences(preferences) {
    try {
        const loadingDiv = document.getElementById('charactersGrid');
        if (loadingDiv) {
            loadingDiv.innerHTML = '<div class="loading">Creating your AI companion...</div>';
        }
        
        const character = await createCharacter({ preferences });
        
        if (character && character.id) {
            navigateTo(`/character?id=${character.id}`);
        } else {
            alert('Character created but could not redirect. Please refresh the page.');
            window.location.reload();
        }
    } catch (error) {
        alert('Error creating character: ' + error.message);
        if (document.getElementById('charactersGrid')) {
            loadAndDisplayCharacters();
        }
    }
}

// Delete current character
async function deleteCurrentCharacter() {
    const urlParams = new URLSearchParams(window.location.search);
    const characterId = urlParams.get('id');
    
    if (!characterId) return;
    
    if (!confirm('Are you sure you want to delete this character? This will also delete all chat history.')) {
        return;
    }
    
    const success = await deleteCharacter(characterId);
    
    if (success) {
        alert('Character deleted successfully!');
        navigateTo('/characters');
    } else {
        alert('Error deleting character. Please try again.');
    }
}

// Load and display characters
async function loadAndDisplayCharacters() {
    const container = document.getElementById('charactersGrid');
    if (!container) return;
    
    container.innerHTML = '<div class="loading">Loading characters...</div>';
    
    const characters = await loadCharacters();
    displayCharacters(characters, 'charactersGrid');
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export functions to window
window.navigateTo = navigateTo;
window.loadCharacters = loadCharacters;
window.loadCharacter = loadCharacter;
window.createCharacter = createCharacter;
window.deleteCharacter = deleteCharacter;
window.displayCharacters = displayCharacters;
window.displayCharacterDetails = displayCharacterDetails;
window.showCreateCharacterModal = showCreateCharacterModal;
window.createCharacterWithPreferences = createCharacterWithPreferences;
window.deleteCurrentCharacter = deleteCurrentCharacter;
window.loadAndDisplayCharacters = loadAndDisplayCharacters;

// Form submission handler
document.getElementById('generatorForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const generateBtn = document.getElementById('generateBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const btnLoader = generateBtn.querySelector('.btn-loader');
    
    // Disable button and show loading
    generateBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    
    // Get form data
    const formData = {
        preferences: {
            name: document.getElementById('name').value.trim(),
            personality: document.getElementById('personality').value,
            appearance: document.getElementById('appearance').value,
            interests: document.getElementById('interests').value.trim() || 'various',
            age: document.getElementById('age').value
        }
    };
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayGirlfriend(data.girlfriend);
            loadRecentGirlfriends();
        } else {
            showError(data.error || 'Failed to generate AI girlfriend');
        }
    } catch (error) {
        showError('An error occurred: ' + error.message);
    } finally {
        // Re-enable button
        generateBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
});

function displayGirlfriend(girlfriend) {
    const resultSection = document.getElementById('resultSection');
    const girlfriendCard = document.getElementById('girlfriendCard');
    
    girlfriendCard.innerHTML = `
        <h3>${girlfriend.name}</h3>
        <div class="info-item">
            <div class="info-label">Personality</div>
            <div class="info-value">${girlfriend.personality}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Appearance</div>
            <div class="info-value">${girlfriend.appearance}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Interests</div>
            <div class="info-value">${girlfriend.interests}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Backstory</div>
            <div class="info-value">${girlfriend.backstory}</div>
        </div>
    `;
    
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    const resultSection = document.getElementById('resultSection');
    const girlfriendCard = document.getElementById('girlfriendCard');
    
    girlfriendCard.innerHTML = `<div class="error">${message}</div>`;
    resultSection.style.display = 'block';
}

async function loadRecentGirlfriends() {
    try {
        const response = await fetch('/api/girlfriends');
        const data = await response.json();
        
        if (data.success && data.girlfriends) {
            displayRecentGirlfriends(data.girlfriends);
        }
    } catch (error) {
        console.error('Error loading recent girlfriends:', error);
    }
}

function displayRecentGirlfriends(girlfriends) {
    const container = document.getElementById('recentGirlfriends');
    
    if (girlfriends.length === 0) {
        container.innerHTML = '<p>No recent generations yet. Create your first AI girlfriend!</p>';
        return;
    }
    
    container.innerHTML = girlfriends.map(gf => `
        <div class="girlfriend-mini-card" onclick="viewGirlfriend(${gf.id})">
            <h4>${gf.name}</h4>
            <p><strong>Personality:</strong> ${gf.personality}</p>
            <p><strong>Interests:</strong> ${gf.interests}</p>
        </div>
    `).join('');
}

async function viewGirlfriend(id) {
    try {
        const response = await fetch(`/api/girlfriend/${id}`);
        const data = await response.json();
        
        if (data.success) {
            displayGirlfriend(data.girlfriend);
        }
    } catch (error) {
        console.error('Error loading girlfriend:', error);
    }
}

// Load recent girlfriends on page load
loadRecentGirlfriends();

// API Configuration
const API_BASE_URL = 'http://localhost:5001/api/auth';
const PREDICTION_API_URL = 'http://localhost:5001/api/predict';

// ASL Alphabet mapping - using full URL to ensure images load correctly
const ASL_ALPHABET = {
    'a': 'http://localhost:5001/Alphabet/A.png',
    'b': 'http://localhost:5001/Alphabet/B.png',
    'c': 'http://localhost:5001/Alphabet/C.png',
    'd': 'http://localhost:5001/Alphabet/D.png',
    'e': 'http://localhost:5001/Alphabet/E.png',
    'f': 'http://localhost:5001/Alphabet/F.png',
    'g': 'http://localhost:5001/Alphabet/G.png',
    'h': 'http://localhost:5001/Alphabet/H.png',
    'i': 'http://localhost:5001/Alphabet/I.png',
    'j': 'http://localhost:5001/Alphabet/J.png',
    'k': 'http://localhost:5001/Alphabet/K.png',
    'l': 'http://localhost:5001/Alphabet/L.png',
    'm': 'http://localhost:5001/Alphabet/M.png',
    'n': 'http://localhost:5001/Alphabet/N.png',
    'o': 'http://localhost:5001/Alphabet/O.png',
    'p': 'http://localhost:5001/Alphabet/P.png',
    'q': 'http://localhost:5001/Alphabet/Q.png',
    'r': 'http://localhost:5001/Alphabet/R.png',
    's': 'http://localhost:5001/Alphabet/S.png',
    't': 'http://localhost:5001/Alphabet/T.png',
    'u': 'http://localhost:5001/Alphabet/U.png',
    'v': 'http://localhost:5001/Alphabet/V.png',
    'w': 'http://localhost:5001/Alphabet/W.png',
    'x': 'http://localhost:5001/Alphabet/X.png',
    'y': 'http://localhost:5001/Alphabet/Y.png',
    'z': 'http://localhost:5001/Alphabet/Z.png'
};

// Word explanation mapping
const WORD_EXPLANATIONS = {
    'A': 'The letter A in ASL is made by forming a fist with your thumb pressed against the side of your index finger.',
    'B': 'The letter B is made by holding all four fingers straight up together and your thumb folded across your palm.',
    'C': 'The letter C is made by curving your fingers to form a C shape, with your thumb and fingers creating a half-circle.',
    'D': 'The letter D is made by pointing your index finger up, with your thumb and other fingers forming a circle.',
    'E': 'The letter E is made by curling all fingers into your palm, with your thumb folded across them.',
    'F': 'The letter F is made by touching your thumb to your index finger, with your other three fingers extended.',
    'G': 'The letter G is made by pointing your index finger to the side, with your thumb and other fingers curled.',
    'H': 'The letter H is made by pointing your index and middle fingers to the side, with your thumb and other fingers curled.',
    'I': 'The letter I is made by extending your pinky finger up, with your thumb and other fingers curled into your palm.',
    'J': 'The letter J is made by extending your pinky finger and drawing a J shape in the air.',
    'K': 'The letter K is made by pointing your index and middle fingers up in a V shape, with your thumb between them.',
    'L': 'The letter L is made by extending your thumb and index finger to form an L shape.',
    'M': 'The letter M is made by tucking your thumb under your three middle fingers, which are folded down.',
    'N': 'The letter N is made by tucking your thumb under your index and middle fingers, which are folded down.',
    'O': 'The letter O is made by forming a circle with your thumb and fingers touching.',
    'P': 'The letter P is made by pointing your index finger down, with your thumb and middle finger forming a circle.',
    'Q': 'The letter Q is made by pointing your index finger down and to the side, with your thumb and middle finger forming a circle.',
    'R': 'The letter R is made by crossing your index and middle fingers, with your thumb and other fingers curled.',
    'S': 'The letter S is made by forming a fist with your thumb wrapped over your fingers.',
    'T': 'The letter T is made by tucking your thumb between your index and middle fingers, which are extended.',
    'U': 'The letter U is made by extending your index and middle fingers up together, with your thumb and other fingers curled.',
    'V': 'The letter V is made by extending your index and middle fingers up in a V shape, with your thumb and other fingers curled.',
    'W': 'The letter W is made by extending your thumb, index, and middle fingers up, with your ring and pinky fingers curled.',
    'X': 'The letter X is made by curling your index finger, with your thumb and other fingers extended.',
    'Y': 'The letter Y is made by extending your thumb and pinky finger, with your other fingers curled.',
    'Z': 'The letter Z is made by pointing your index finger and drawing a Z shape in the air.'
};

// YouTube Videos Data
const YOUTUBE_VIDEOS = [
    {
        id: '0FcwzMq4iWg',
        title: 'ASL Learning Video 1',
        url: 'https://youtu.be/0FcwzMq4iWg?si=UXW3a4_adDHXCDf2'
    },
    {
        id: 'DBQINq0SsAw',
        title: 'ASL Learning Video 2',
        url: 'https://youtu.be/DBQINq0SsAw?si=-7TQjn93IRvCjuSW'
    },
    {
        id: '_c--P6VRTUo',
        title: 'ASL Learning Video 3',
        url: 'https://youtu.be/_c--P6VRTUo?si=Y0rKaqfe2BrfM8KS'
    }
];

// Application State
const app = {
    authToken: null,
    currentUser: null,
    currentView: 'home',
    likedVideos: new Set() // Track liked videos
};

// DOM Elements
const elements = {
    authContainer: document.getElementById('auth-container'),
    app: document.getElementById('app'),
    loginForm: document.getElementById('login-form-element'),
    signupForm: document.getElementById('signup-form-element'),
    loginError: document.getElementById('login-error'),
    signupError: document.getElementById('signup-error'),
    logoutBtn: document.getElementById('logout-btn'),
    userInfo: document.getElementById('user-info'),
    navItems: document.querySelectorAll('.nav-item'),
    views: document.querySelectorAll('.view'),
    tabBtns: document.querySelectorAll('.tab-btn'),
    // History elements
    historyList: document.getElementById('history-list'),
    refreshHistoryBtn: document.getElementById('refresh-history-btn'),
    // Videos grid
    videosGrid: document.getElementById('videos-grid'),
    // Alphabet guide
    alphabetGrid: document.getElementById('alphabet-grid'),
    // AI Generator
    llmInput: document.getElementById('llm-input'),
    llmGenerateBtn: document.getElementById('llm-generate-btn'),
    llmSpinner: document.getElementById('llm-spinner'),
    llmOutput: document.getElementById('llm-output'),
    llmImageContainer: document.getElementById('llm-image-container'),
    // Launch detection
    launchDetectionBtn: document.getElementById('launch-detection-btn')
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeAuth();
    initializeNavigation();
    initializeDetection();
    initializeHistory();
    initializeAlphabet();
    initializeGenerator();
    initializeVideos();
    checkAuthState();
});

// Authentication Functions
function initializeAuth() {
    // Tab switching
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            elements.tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            document.querySelectorAll('.auth-form').forEach(form => form.classList.remove('active'));
            document.getElementById(`${tab}-form`).classList.add('active');
            
            // Clear errors
            elements.loginError.textContent = '';
            elements.signupError.textContent = '';
        });
    });

    // Login form
    elements.loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                app.authToken = data.token;
                app.currentUser = data.user;
                localStorage.setItem('authToken', app.authToken);
                showDashboard();
            } else {
                elements.loginError.textContent = data.message || 'Login failed';
            }
        } catch (error) {
            elements.loginError.textContent = 'Connection error. Please check if backend is running.';
            console.error('Login error:', error);
        }
    });

    // Signup form
    elements.signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('signup-name').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        
        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                app.authToken = data.token;
                app.currentUser = data.user;
                localStorage.setItem('authToken', app.authToken);
                showDashboard();
            } else {
                elements.signupError.textContent = data.message || 'Registration failed';
            }
        } catch (error) {
            elements.signupError.textContent = 'Connection error. Please check if backend is running.';
            console.error('Signup error:', error);
        }
    });

    // Logout
    elements.logoutBtn.addEventListener('click', () => {
        app.authToken = null;
        app.currentUser = null;
        localStorage.removeItem('authToken');
        stopCamera();
        showAuth();
    });
}

function checkAuthState() {
    const token = localStorage.getItem('authToken');
    if (token) {
        app.authToken = token;
        // Verify token by fetching user info
        fetch(`${API_BASE_URL}/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(res => res.json())
        .then(data => {
            if (data.user) {
                app.currentUser = data.user;
                showDashboard();
            } else {
                localStorage.removeItem('authToken');
                showAuth();
            }
        })
        .catch(() => {
            localStorage.removeItem('authToken');
            showAuth();
        });
    } else {
        showAuth();
    }
}

function showAuth() {
    elements.authContainer.classList.remove('hidden');
    elements.app.classList.add('hidden');
}

function showDashboard() {
    elements.authContainer.classList.add('hidden');
    elements.app.classList.remove('hidden');
    if (app.currentUser) {
        elements.userInfo.textContent = app.currentUser.email || app.currentUser.name || 'User';
    }
    populateVideos();
}

// Navigation Functions
function initializeNavigation() {
    elements.navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const view = item.dataset.view;
            app.showView(view);
        });
    });
}

app.showView = function(view) {
    // Update active nav item
    elements.navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.view === view);
    });
    
    // Update active view
    elements.views.forEach(v => {
        v.classList.toggle('active', v.id === `${view}-view`);
    });
    
    app.currentView = view;
    
    // Load view-specific data
    if (view === 'history') {
        loadHistory();
    } else if (view === 'alphabet') {
        populateAlphabetGuide();
    } else if (view === 'generator') {
        // Generator is ready
    } else if (view === 'detection') {
        // Detection view ready
    } else if (view === 'home') {
        populateVideos();
    }
};

// Detection Functions
function initializeDetection() {
    if (elements.launchDetectionBtn) {
        elements.launchDetectionBtn.addEventListener('click', launchDetectionApp);
    }
}

async function launchDetectionApp() {
    const btn = elements.launchDetectionBtn;
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Launching...';
    }
    
    try {
        const response = await fetch('http://localhost:5001/api/launch-detection', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✅ Detection application launched successfully!\n\nThe sign language detection window should open in a new terminal window.');
        } else {
            alert(`⚠️ ${data.message || data.error || 'Failed to launch. Please run manually:\n\ncd Sign-Language\n.\\venv\\Scripts\\python.exe final_pred.py'}`);
        }
    } catch (error) {
        console.error('Error launching detection app:', error);
        alert('⚠️ Could not launch automatically.\n\nPlease run manually:\n1. Open a terminal\n2. cd Sign-Language\n3. .\\venv\\Scripts\\python.exe final_pred.py');
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '🚀 Launch Detection App';
        }
    }
}

// Alphabet Guide Functions
function initializeAlphabet() {
    // Alphabet guide will be populated when view is shown
}

function populateAlphabetGuide() {
    if (!elements.alphabetGrid) return;
    
    elements.alphabetGrid.innerHTML = '';
    Object.entries(ASL_ALPHABET).forEach(([letter, imageUrl]) => {
        const card = document.createElement('div');
        card.className = 'alphabet-card-container';
        card.setAttribute('data-letter', letter.toUpperCase());
        
        // Create image element with error handling
        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = `Sign for ${letter}`;
        img.className = 'sign-image';
        img.onerror = function() {
            console.error(`Failed to load image for letter ${letter}: ${imageUrl}`);
            this.style.display = 'none';
            const errorMsg = document.createElement('div');
            errorMsg.textContent = 'Image not found';
            errorMsg.style.color = '#999';
            this.parentElement.appendChild(errorMsg);
        };
        
        card.innerHTML = `
            <div class="alphabet-card w-full">
                <div class="card-face card-front">
                    <span class="text-6xl font-bold">${letter.toUpperCase()}</span>
                </div>
                <div class="card-face card-back">
                </div>
            </div>
        `;
        
        // Append image to card-back
        const cardBack = card.querySelector('.card-back');
        cardBack.appendChild(img);
        
        card.addEventListener('click', () => {
            card.querySelector('.alphabet-card').classList.toggle('is-flipped');
        });
        elements.alphabetGrid.appendChild(card);
    });
}

// AI Generator Functions
function initializeGenerator() {
    if (elements.llmGenerateBtn) {
        elements.llmGenerateBtn.addEventListener('click', generateSignExplanation);
    }
}

async function generateSignExplanation() {
    const query = elements.llmInput.value.trim().toLowerCase();
    if (!query) {
        alert('Please enter a word or phrase.');
        return;
    }

    elements.llmGenerateBtn.disabled = true;
    elements.llmSpinner.classList.remove('hidden');
    elements.llmOutput.innerHTML = '<p class="text-center text-gray-500">Generating explanation...</p>';
    elements.llmImageContainer.innerHTML = '';

    try {
        // Call the explain API
        const response = await fetch('http://localhost:5001/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        const explanation = data.answer || 'Failed to get explanation.';

        elements.llmOutput.innerHTML = `<p>${explanation.replace(/\n/g, '<br>')}</p>`;

        // Save to queries if logged in
        if (app.authToken) {
            try {
                await fetch(`${API_BASE_URL}/queries`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${app.authToken}`
                    },
                    body: JSON.stringify({
                        query: query,
                        explanation: explanation,
                        timestamp: new Date().toISOString()
                    })
                });
            } catch (error) {
                console.error('Error saving query:', error);
            }
        }

        // Show fingerspelling images
        const words = query.split(/\s+/);
        let totalDelay = 0;
        const wordDelay = 1500;
        
        for (const word of words) {
            if (word) {
                const letters = word.split('');
                for (const char of letters) {
                    const imageUrl = ASL_ALPHABET[char];
                    if (imageUrl) {
                        setTimeout(() => {
                            const img = document.createElement('img');
                            img.src = imageUrl;
                            img.alt = `Sign for ${char}`;
                            img.className = 'w-24 h-24 object-contain rounded-lg shadow-md';
                            elements.llmImageContainer.appendChild(img);
                        }, totalDelay);
                        totalDelay += 500;
                    }
                }
            }
            totalDelay += wordDelay;
        }
    } catch (error) {
        console.error('Error generating explanation:', error);
        elements.llmOutput.innerHTML = '<p class="text-center text-red-500">Failed to get explanation. Please check if backend is running.</p>';
    }

    elements.llmGenerateBtn.disabled = false;
    elements.llmSpinner.classList.add('hidden');
}

async function savePredictionToHistory(prediction) {
    if (!app.authToken) return;
    
    const explanation = WORD_EXPLANATIONS[prediction] || `The letter ${prediction} in American Sign Language.`;
    
    try {
        await fetch(`${API_BASE_URL}/history`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${app.authToken}`
            },
            body: JSON.stringify({
                prediction,
                explanation,
                timestamp: new Date().toISOString()
            })
        });
        
        // Update stats if on dashboard
        if (app.currentView === 'home') {
            updateDashboardStats();
        }
    } catch (error) {
        console.error('Error saving prediction:', error);
    }
}

// History Functions
function initializeHistory() {
    elements.refreshHistoryBtn.addEventListener('click', loadHistory);
}

async function loadHistory() {
    if (!app.authToken) {
        elements.historyList.innerHTML = '<div class="loading-state">Please log in to view history</div>';
        return;
    }
    
    elements.historyList.innerHTML = '<div class="loading-state">Loading history...</div>';
    
    try {
        // Load queries (searched words) from AI Generator
        const queriesResponse = await fetch(`${API_BASE_URL}/queries`, {
            headers: { 'Authorization': `Bearer ${app.authToken}` }
        });
        
        const queriesData = await queriesResponse.json();
        
        // Also load predictions if needed
        const predictionsResponse = await fetch(`${API_BASE_URL}/history`, {
            headers: { 'Authorization': `Bearer ${app.authToken}` }
        });
        
        const predictionsData = await predictionsResponse.json();
        
        // Combine and sort by timestamp
        const allItems = [];
        
        if (queriesData.queries && queriesData.queries.length > 0) {
            queriesData.queries.forEach(item => {
                allItems.push({
                    word: item.query,
                    explanation: item.explanation,
                    timestamp: item.timestamp,
                    type: 'search'
                });
            });
        }
        
        if (predictionsData.history && predictionsData.history.length > 0) {
            predictionsData.history.forEach(item => {
                const isVideo = item.prediction && item.prediction.startsWith('VIDEO:');
                allItems.push({
                    word: item.prediction,
                    explanation: item.explanation,
                    timestamp: item.timestamp,
                    type: isVideo ? 'video' : 'prediction',
                    url: item.explanation && item.explanation.includes('URL:') 
                        ? item.explanation.split('URL:')[1].trim() 
                        : null
                });
            });
        }
        
        // Sort by timestamp (newest first)
        allItems.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        if (allItems.length > 0) {
            elements.historyList.innerHTML = allItems.map(item => {
                const date = new Date(item.timestamp);
                let typeLabel = '🎯 Detected';
                if (item.type === 'search') typeLabel = '🔍 Searched';
                else if (item.type === 'video') typeLabel = '❤️ Liked Video';
                
                const wordDisplay = item.type === 'video' 
                    ? item.word.replace('VIDEO: ', '') 
                    : item.word.toUpperCase();
                
                const explanationHtml = item.url 
                    ? `${item.explanation.split('URL:')[0].trim()}<br><a href="${item.url}" target="_blank" style="color: var(--accent-primary); text-decoration: none; margin-top: 0.5rem; display: inline-block;">▶ Watch Video</a>`
                    : item.explanation;
                
                return `
                    <div class="history-item">
                        <div class="history-item-header">
                            <span class="history-prediction">${wordDisplay}</span>
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 0.75rem; color: var(--text-secondary);">${typeLabel}</span>
                                <span class="history-timestamp">${formatDate(date)}</span>
                            </div>
                        </div>
                        <div class="history-explanation">${explanationHtml}</div>
                    </div>
                `;
            }).join('');
        } else {
            elements.historyList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📭</div>
                    <p>No history yet. Search for words or detect signs to build your history!</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading history:', error);
        elements.historyList.innerHTML = '<div class="loading-state">Error loading history</div>';
    }
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Videos Functions
function initializeVideos() {
    // Load liked videos from localStorage
    const savedLikes = localStorage.getItem('likedVideos');
    if (savedLikes) {
        try {
            app.likedVideos = new Set(JSON.parse(savedLikes));
        } catch (e) {
            app.likedVideos = new Set();
        }
    }
}

// Create pop sound using Web Audio API
function playPopSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (error) {
        console.log('Could not play pop sound:', error);
    }
}

function populateVideos() {
    if (!elements.videosGrid) return;
    
    elements.videosGrid.innerHTML = YOUTUBE_VIDEOS.map((video, index) => {
        const thumbnailUrl = `https://img.youtube.com/vi/${video.id}/maxresdefault.jpg`;
        const isLiked = app.likedVideos.has(video.id);
        
        return `
            <div class="video-card" data-video-id="${video.id}">
                <div class="video-thumbnail-container" onclick="window.open('${video.url}', '_blank')">
                    <img src="${thumbnailUrl}" alt="${video.title}" class="video-thumbnail" 
                         onerror="this.src='https://img.youtube.com/vi/${video.id}/hqdefault.jpg'">
                    <div class="video-play-button"></div>
                </div>
                <div class="video-info">
                    <div class="video-title">
                        <span class="video-title-text">${video.title}</span>
                        <button class="video-like-btn ${isLiked ? 'liked' : ''}" 
                                data-video-id="${video.id}" 
                                data-video-title="${video.title.replace(/"/g, '&quot;')}"
                                data-video-url="${video.url}">
                            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    // Add event listeners to like buttons
    elements.videosGrid.querySelectorAll('.video-like-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const videoId = btn.dataset.videoId;
            const videoTitle = btn.dataset.videoTitle;
            const videoUrl = btn.dataset.videoUrl;
            handleVideoLike(e, videoId, videoTitle, videoUrl);
        });
    });
}

function handleVideoLike(event, videoId, videoTitle, videoUrl) {
    event.stopPropagation();
    
    const likeBtn = event.target.closest('.video-like-btn');
    const isLiked = app.likedVideos.has(videoId);
    
    if (isLiked) {
        // Unlike
        app.likedVideos.delete(videoId);
        likeBtn.classList.remove('liked');
    } else {
        // Like
        app.likedVideos.add(videoId);
        likeBtn.classList.add('liked');
        
        // Play pop sound
        playPopSound();
        
        // Create flying heart animation
        createFlyingHeart(event);
        
        // Save to history
        saveVideoToHistory(videoId, videoTitle, videoUrl);
    }
    
    // Save to localStorage
    localStorage.setItem('likedVideos', JSON.stringify(Array.from(app.likedVideos)));
}

function createFlyingHeart(event) {
    const heart = document.createElement('div');
    heart.className = 'flying-heart';
    heart.innerHTML = '❤️';
    
    const rect = event.target.getBoundingClientRect();
    heart.style.left = rect.left + rect.width / 2 + 'px';
    heart.style.top = rect.top + rect.height / 2 + 'px';
    
    document.body.appendChild(heart);
    
    // Remove after animation
    setTimeout(() => {
        heart.remove();
    }, 1500);
}

async function saveVideoToHistory(videoId, videoTitle, videoUrl) {
    if (!app.authToken) return;
    
    const explanation = `Liked video: ${videoTitle}`;
    
    try {
        // Save as a special type of history item
        await fetch(`${API_BASE_URL}/history`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${app.authToken}`
            },
            body: JSON.stringify({
                prediction: `VIDEO: ${videoTitle}`,
                explanation: `${explanation}\nURL: ${videoUrl}`,
                timestamp: new Date().toISOString(),
                type: 'video'
            })
        });
    } catch (error) {
        console.error('Error saving video to history:', error);
    }
}

// Make app available globally for onclick handlers
window.app = app;



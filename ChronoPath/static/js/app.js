// ChronoPath AI - SPA Client Controller

document.addEventListener('DOMContentLoaded', () => {
    // Local In-Memory History Cache
    const visitedTimeline = [];

    // DOM Elements
    const mainHeader = document.getElementById('main-header');
    const userDisplay = document.getElementById('user-display');
    const logoutBtn = document.getElementById('logout-btn');

    const loginView = document.getElementById('login-view');
    const dashboardView = document.getElementById('dashboard-view');

    const authTitle = document.getElementById('auth-title');
    const authSubtitle = document.getElementById('auth-subtitle');

    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginError = document.getElementById('login-error');
    const loginErrorText = document.getElementById('login-error-text');

    const registerForm = document.getElementById('register-form');
    const regUsernameInput = document.getElementById('reg-username');
    const regPasswordInput = document.getElementById('reg-password');
    const registerError = document.getElementById('register-error');
    const registerErrorText = document.getElementById('register-error-text');

    const showRegisterBtn = document.getElementById('show-register-btn');
    const showLoginBtn = document.getElementById('show-login-btn');

    const latInput = document.getElementById('lat');
    const lngInput = document.getElementById('lng');
    const ageInput = document.getElementById('age');
    const originInput = document.getElementById('origin');
    const backgroundInput = document.getElementById('background');
    const languageSelect = document.getElementById('language');
    const networkSelect = document.getElementById('network');

    const geoBtn = document.getElementById('geo-btn');
    const generateBtn = document.getElementById('generate-btn');

    const loaderView = document.getElementById('chronicle-loader');
    const idleView = document.getElementById('chronicle-idle');
    const contentView = document.getElementById('chronicle-content');

    const eraBadge = document.getElementById('chronicle-era');
    const chronicleTitle = document.getElementById('chronicle-title');
    const visualFrame = document.getElementById('chronicle-visual-frame');
    const chronicleVisual = document.getElementById('chronicle-visual');
    const chronicleStory = document.getElementById('chronicle-story');
    const audioPanel = document.getElementById('chronicle-audio-panel');
    const chronicleAudio = document.getElementById('chronicle-audio');

    const noteConfidence = document.getElementById('note-confidence');
    const noteLatency = document.getElementById('note-latency');
    const noteCache = document.getElementById('note-cache');
    const noteFacts = document.getElementById('note-facts');
    const timelineList = document.getElementById('timeline-list');

    // SPA Router / View Manager
    function checkAuth() {
        const token = localStorage.getItem('access_token');
        const username = localStorage.getItem('username');

        if (token && username) {
            userDisplay.textContent = `Explorer: ${username}`;
            loginView.classList.add('hidden');
            mainHeader.classList.remove('hidden');
            dashboardView.classList.remove('hidden');
        } else {
            mainHeader.classList.add('hidden');
            dashboardView.classList.add('hidden');
            loginView.classList.remove('hidden');
            localStorage.clear();
        }
    }

    // Toggle between Login and Register Forms
    showRegisterBtn.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        authTitle.textContent = "Registry Sign-Up";
        authSubtitle.textContent = "Write your name in the annals of exploration";
        loginError.classList.add('hidden');
    });

    showLoginBtn.addEventListener('click', (e) => {
        e.preventDefault();
        registerForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
        authTitle.textContent = "Chronicle Registry";
        authSubtitle.textContent = "Sign the Guestbook to unlock the pathways of history";
        registerError.classList.add('hidden');
    });

    // FORM-URLENCODED LOGIN REQUEST
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        loginError.classList.add('hidden');
        loginForm.classList.add('loading');

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        // OAuth2 Password Grant requires application/x-www-form-urlencoded
        const bodyParams = new URLSearchParams();
        bodyParams.append('username', username);
        bodyParams.append('password', password);

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: bodyParams
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('username', data.username);
                passwordInput.value = '';
                checkAuth();
            } else {
                loginErrorText.textContent = data.detail || 'Access keyphrase rejected.';
                loginError.classList.remove('hidden');
            }
        } catch (err) {
            loginErrorText.textContent = 'Server Registry offline. Please start uvicorn.';
            loginError.classList.remove('hidden');
        } finally {
            loginForm.classList.remove('loading');
        }
    });

    // JSON REGISTER REQUEST
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        registerError.classList.add('hidden');
        registerForm.classList.add('loading');

        const username = regUsernameInput.value.trim();
        const password = regPasswordInput.value.trim();

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('username', data.username);
                regUsernameInput.value = '';
                regPasswordInput.value = '';
                // Return registry back to login form state for next logout
                showLoginBtn.click();
                checkAuth();
            } else {
                registerErrorText.textContent = data.detail || 'Registration rejected.';
                registerError.classList.remove('hidden');
            }
        } catch (err) {
            registerErrorText.textContent = 'Failed to connect to registry server.';
            registerError.classList.remove('hidden');
        } finally {
            registerForm.classList.remove('loading');
        }
    });

    // LOGOUT
    logoutBtn.addEventListener('click', () => {
        localStorage.clear();
        checkAuth();
        // Clear session narrative items
        visitedTimeline.length = 0;
        renderTimeline();
        // Reset state view
        idleView.classList.remove('hidden');
        contentView.classList.add('hidden');
        loaderView.classList.add('hidden');
    });

    // GEOLOCATION COMPASS DIAL
    geoBtn.addEventListener('click', () => {
        if (!navigator.geolocation) {
            alert('Your browser does not support geolocation lookup.');
            return;
        }

        geoBtn.textContent = 'Consulting Sky...';
        geoBtn.disabled = true;

        navigator.geolocation.getCurrentPosition(
            (position) => {
                latInput.value = position.coords.latitude.toFixed(4);
                lngInput.value = position.coords.longitude.toFixed(4);
                geoBtn.textContent = 'Consult Compass';
                geoBtn.disabled = false;
            },
            (error) => {
                alert(`Compass error: ${error.message}`);
                geoBtn.textContent = 'Consult Compass';
                geoBtn.disabled = false;
            },
            { enableHighAccuracy: true, timeout: 5000 }
        );
    });

    // INVOKE CHRONICLE (POST GENERATE)
    generateBtn.addEventListener('click', async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            checkAuth();
            return;
        }

        const lat = parseFloat(latInput.value);
        const lng = parseFloat(lngInput.value);
        const age = ageInput.value ? parseInt(ageInput.value) : null;
        const origin = originInput.value.trim() || null;
        const background = backgroundInput.value.trim() || null;
        const language = languageSelect.value;
        const network = networkSelect.value;

        // Visual states update
        idleView.classList.add('hidden');
        contentView.classList.add('hidden');
        loaderView.classList.remove('hidden');

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    user_id: localStorage.getItem('username'),
                    latitude: lat,
                    longitude: lng,
                    language: language,
                    age: age,
                    origin: origin,
                    background: background,
                    network_quality: network
                })
            });

            if (response.status === 401) {
                // Token expired or invalid
                alert('Session expired. Please sign the registry guestbook again.');
                logoutBtn.click();
                return;
            }

            const data = await response.json();

            if (response.ok) {
                renderChronicle(data);
                
                // Add to internal session history cache
                const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                visitedTimeline.unshift({
                    place: data.place.name || 'Landmark',
                    timestamp: timestamp,
                    data: data
                });
                renderTimeline();
            } else {
                alert(`Archive connection error: ${data.detail || 'Unknown failure'}`);
                idleView.classList.remove('hidden');
            }
        } catch (err) {
            alert('Failed to connect to the backend server.');
            idleView.classList.remove('hidden');
        } finally {
            loaderView.classList.add('hidden');
        }
    });

    // RENDER GENERATED CHRONICLE CONTENT
    function renderChronicle(data) {
        contentView.classList.remove('hidden');

        // Text title & story
        chronicleTitle.textContent = data.text.title || 'Unknown Landmark';
        chronicleStory.textContent = data.text.story || 'No narrative text generated.';
        
        // Era badge lookup (or fall back to place id)
        eraBadge.textContent = data.place.id || 'Landmark';

        // Render Visual if available
        if (data.visual && data.visual.url && data.visual.url.trim() !== '') {
            chronicleVisual.src = data.visual.url;
            visualFrame.classList.remove('hidden');
        } else {
            visualFrame.classList.add('hidden');
            chronicleVisual.src = '';
        }

        // Render Audio if available
        if (data.audio && data.audio.url && data.audio.url.trim() !== '') {
            chronicleAudio.src = data.audio.url;
            chronicleAudio.load();
            audioPanel.classList.remove('hidden');
        } else {
            audioPanel.classList.add('hidden');
            chronicleAudio.src = '';
        }

        // Registry notes/metadata
        if (data.meta) {
            noteLatency.textContent = `${data.meta.latency_ms} ms`;
            noteCache.textContent = data.meta.cache_hit === 'true' ? 'Cached Record' : 'Fresh Compile';
        } else {
            noteLatency.textContent = 'N/A';
            noteCache.textContent = 'Fresh Compile';
        }

        // Grounding facts listing
        noteFacts.innerHTML = '';
        const facts = (data.text.story && data.text.story.includes('Welcome to Unknown Location')) 
            ? ['No regional historical context matching coordinates.']
            : (data.text.facts || ['This landmark has verified historical significance.']);
        
        // Fallback facts display logic
        if (facts.length === 0) {
            const li = document.createElement('li');
            li.textContent = 'Grounded in historical database context.';
            noteFacts.appendChild(li);
        } else {
            facts.forEach(fact => {
                const li = document.createElement('li');
                li.textContent = fact;
                noteFacts.appendChild(li);
            });
        }
        
        // Adjust confidence representation
        noteConfidence.textContent = data.safe ? 'High Safety Rating (Verified)' : 'Pending Review';
    }

    // RENDER TIMELINE HISTORY SCROLL
    function renderTimeline() {
        timelineList.innerHTML = '';

        if (visitedTimeline.length === 0) {
            const span = document.createElement('span');
            span.className = 'empty-timeline';
            span.textContent = 'No history recorded in this session.';
            timelineList.appendChild(span);
            return;
        }

        visitedTimeline.forEach((item, index) => {
            const div = document.createElement('div');
            div.className = 'timeline-item';
            div.addEventListener('click', () => {
                renderChronicle(item.data);
            });

            const placeSpan = document.createElement('span');
            placeSpan.className = 'item-place';
            placeSpan.textContent = item.place;

            const timeSpan = document.createElement('span');
            timeSpan.className = 'item-date';
            timeSpan.textContent = item.timestamp;

            div.appendChild(placeSpan);
            div.appendChild(timeSpan);
            timelineList.appendChild(div);
        });
    }

    // Initialize check
    checkAuth();
});

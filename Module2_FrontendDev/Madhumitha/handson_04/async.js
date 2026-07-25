// ============================================================
// Digital Nurture 5.0 | Frontend HO4 | async.js
// Async JavaScript, Fetch API & Axios Integration
// Author: Madhumitha R
// This file is loaded as type="module" in ho4_index.html
// ============================================================

const BASE = 'https://jsonplaceholder.typicode.com';

// Import local courses for fallback
const localCourses = [
    { id:1, name:'Data Structures & Algorithms', code:'CS101', credits:4, grade:'A' },
    { id:2, name:'Database Management Systems',  code:'CS102', credits:3, grade:'B' },
    { id:3, name:'Object Oriented Programming',  code:'CS103', credits:4, grade:'A' },
    { id:4, name:'Web Development Fundamentals', code:'CS104', credits:3, grade:'B' },
    { id:5, name:'Python for Data Science',      code:'CS105', credits:4, grade:'A' }
];

// ============================================================
// TASK 1: PROMISES & ASYNC/AWAIT (Steps 45–49)
// ============================================================

// Step 45: Promise-chain version
function fetchUserPromise(id) {
    return fetch(`${BASE}/users/${id}`)
        .then(res => res.json())
        .then(user => { console.log('Promise chain user:', user.name); return user; });
}

// Step 46: async/await version — same result, cleaner syntax
async function fetchUser(id) {
    try {
        const res  = await fetch(`${BASE}/users/${id}`);
        const user = await res.json();
        console.log('async/await user:', user.name);
        return user;
    } catch (err) {
        console.error('fetchUser failed:', err.message);
    }
}

// Step 47: Simulate network delay with local data
function fetchAllCourses() {
    return new Promise(resolve => {
        setTimeout(() => resolve(localCourses), 1000);
    });
}

// Step 48: Show loading → render cards after resolve
async function loadCourses() {
    const grid    = document.querySelector('.course-grid');
    const loading = document.getElementById('loading-msg');

    loading.style.display = 'block';
    grid.innerHTML = '';

    const courses = await fetchAllCourses();   // waits 1 second

    loading.style.display = 'none';
    renderCourseCards(courses, grid);
}

// Step 49: Promise.all — fire both requests simultaneously
async function fetchTwoUsers() {
    const [u1, u2] = await Promise.all([
        fetch(`${BASE}/users/1`).then(r => r.json()),
        fetch(`${BASE}/users/2`).then(r => r.json())
    ]);
    // Promise.all is faster than: await fetch(1); await fetch(2);
    // because both requests run in parallel
    console.log('Promise.all result:', u1.name, '&', u2.name);
    document.getElementById('promise-all-result').textContent =
        `Fetched simultaneously: ${u1.name} & ${u2.name}`;
}


// ============================================================
// TASK 2: FETCH WITH ERROR HANDLING (Steps 50–54)
// ============================================================

// Step 50: Reusable fetch wrapper
// WHY: fetch() only rejects on network errors (offline, DNS fail).
// HTTP 404 and 500 still RESOLVE — response.ok catches those.
async function apiFetch(url) {
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText} — ${url}`);
    }
    return res.json();
}

// Step 51–54: Load notifications with loading spinner + error UI + retry
async function loadNotifications() {
    const section = document.getElementById('notifications');
    const spinner = document.getElementById('spinner');
    const retryBtn = document.getElementById('retry-btn');

    section.innerHTML = '';
    spinner.style.display = 'block';
    retryBtn.style.display = 'none';

    try {
        // Step 53: swap to bad URL to trigger error:
        // const posts = await apiFetch(`${BASE}/nonexistent`);
        const posts = await apiFetch(`${BASE}/posts?_limit=5`);
        spinner.style.display = 'none';

        posts.forEach(post => {
            const card = document.createElement('div');
            card.className = 'notification-card';
            card.innerHTML = `<h4>${post.title}</h4><p>${post.body.slice(0, 80)}...</p>`;
            section.appendChild(card);
        });
    } catch (err) {
        // Step 53: friendly error — never just console.error in UI
        spinner.style.display = 'none';
        section.innerHTML = `<p class="error-msg">⚠️ ${err.message}</p>`;
        retryBtn.style.display = 'inline-block';  // Step 54
    }
}

// Step 54: Retry button handler
document.getElementById('retry-btn')?.addEventListener('click', loadNotifications);


// ============================================================
// TASK 3: AXIOS (Steps 55–59)
// Axios loaded via CDN in index.html
// ============================================================

async function loadWithAxios() {
    // Step 58: Request interceptor — logs every request before it fires
    axios.interceptors.request.use(config => {
        console.log(`API call started: ${config.url}`);
        return config;
    });

    // Step 56: axios.get auto-parses JSON; throws on non-2xx automatically
    const { data: posts } = await axios.get(`${BASE}/posts`, {
        params: { userId: 1 },   // Step 57: params object → ?userId=1
        timeout: 5000             // built-in timeout — not available in fetch natively
    });

    console.log(`Axios loaded ${posts.length} posts for userId=1`);
    document.getElementById('axios-result').textContent =
        `Axios fetched ${posts.length} posts for userId=1`;

    /*
     * Step 59: fetch vs Axios — 3 key differences
     * ─────────────────────────────────────────────
     * 1. JSON parsing:
     *    fetch  → manual: await res.json()
     *    axios  → automatic: response.data is already parsed
     *
     * 2. Error handling:
     *    fetch  → only rejects on network error; HTTP 4xx/5xx resolve
     *    axios  → throws on any non-2xx response automatically
     *
     * 3. Extra features:
     *    fetch  → built-in browser API, no install needed
     *    axios  → library; adds: interceptors, timeout, request cancellation,
     *             upload progress events, automatic XSRF protection
     */
}


// ============================================================
// SHARED HELPER — render course cards
// ============================================================
function renderCourseCards(courses, container) {
    const fragment = document.createDocumentFragment();
    courses.forEach(c => {
        const article = document.createElement('article');
        article.className = 'course-card';
        article.innerHTML = `
            <h3>${c.name}</h3>
            <p>Code: <strong>${c.code}</strong></p>
            <div class="card-footer">
                <span class="credits">Credits: ${c.credits}</span>
                <span class="grade grade-${c.grade}">Grade: ${c.grade}</span>
            </div>
        `;
        fragment.appendChild(article);
    });
    container.appendChild(fragment);
}


// ============================================================
// INIT — run everything on page load
// ============================================================
(async () => {
    await fetchUser(1);
    await loadCourses();
    await fetchTwoUsers();
    await loadNotifications();
    await loadWithAxios();
})();

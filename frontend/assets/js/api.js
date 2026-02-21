const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://quran-reading-app-production.up.railway.app';

const ASSETS_BASE_URL = 'https://quran-reading-app.maahermadar.workers.dev';

console.log(`[API] Base URL: ${API_BASE_URL}`);
console.log(`[API] Assets URL: ${ASSETS_BASE_URL}`);

/**
 * Resolves an avatar URL. 
 * Prioritizes the Cloudflare worker path for production-ready assets.
 */
function getAvatarUrl(dbPath) {
    if (!dbPath) return null;
    // Extract filename without extension (e.g., "14" from "/static/avatars/14.jpg")
    const filename = dbPath.split('/').pop();
    const id = filename.split('.')[0];

    // Always use Cloudflare for the frontend as requested
    return `${ASSETS_BASE_URL}/assets/avatars/${id}.webp`;
}

// Simple in-memory cache to prevent flicker on tab switching
// Persistent session cache to prevent flicker on tab switching in MPA
const _apiCache = {
    get: (key) => {
        try {
            const val = sessionStorage.getItem(`api_cache_${key}`);
            return val ? JSON.parse(val) : null;
        } catch (e) { return null; }
    },
    set: (key, data) => {
        try {
            sessionStorage.setItem(`api_cache_${key}`, JSON.stringify(data));
        } catch (e) { }
    },
    has: (key) => !!sessionStorage.getItem(`api_cache_${key}`),
    clear: (key) => {
        if (key) {
            sessionStorage.removeItem(`api_cache_${key}`);
        } else {
            Object.keys(sessionStorage).forEach(k => {
                if (k.startsWith('api_cache_')) sessionStorage.removeItem(k);
            });
        }
    }
};

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('token');

    // Cache GET requests
    const isGet = !options.method || options.method.toUpperCase() === 'GET';
    const cacheKey = endpoint;

    if (isGet && _apiCache.has(cacheKey) && !options.skipCache) {
        return _apiCache.get(cacheKey);
    }

    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    if (response.status === 401 || response.status === 403) {
        localStorage.removeItem('token');
        _apiCache.clear();
        window.location.replace('login.html');
        return;
    }

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || 'API request failed');
    }

    const data = await response.json();

    // Store in cache if it's a GET request
    if (isGet) {
        _apiCache.set(cacheKey, data);
    } else {
        // If we perform a mutation (POST/PUT/DELETE), clear cache to ensure fresh data
        _apiCache.clear();
    }

    return data;
}

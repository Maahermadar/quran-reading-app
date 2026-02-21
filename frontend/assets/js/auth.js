document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Logging in\u2026'; }

    const formData = new FormData();
    formData.append('username', email); // OAuth2PasswordRequestForm uses 'username' field for email
    formData.append('password', password);

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();

        // SECURITY: Always clear all cached API data before switching users.
        // sessionStorage is tab-scoped and NOT user-scoped. Without this,
        // a new user logging in would see the previous user's cached data.
        _apiCache.clear();

        localStorage.setItem('token', data.access_token);
        window.location.href = 'home.html';
    } catch (err) {
        alert('Login Error: ' + err.message);
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Login'; }
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Creating account\u2026'; }

    try {
        await apiFetch('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });

        // Clear any stale cache before directing to login
        _apiCache.clear();

        alert('Registration successful! Please login.');
        window.location.href = 'login.html';
    } catch (err) {
        alert('Registration Error: ' + err.message);
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Create Account'; }
    }
}

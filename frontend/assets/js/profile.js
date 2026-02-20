document.addEventListener('DOMContentLoaded', () => {
    fetchProfile();

    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Wire up avatar upload
    const avatarInput = document.getElementById('avatar-input');
    if (avatarInput) {
        avatarInput.addEventListener('change', handleAvatarUpload);
    }
});

async function fetchProfile() {
    try {
        const data = await apiFetch('/auth/me');
        document.getElementById('user-name-text').textContent = data.name;
        document.getElementById('user-email-text').textContent = data.email;

        // Show avatar image or initial
        applyAvatarToProfilePage(data);
    } catch (err) {
        console.error('Failed to fetch profile:', err);
    }
}

function applyAvatarToProfilePage(data) {
    const profileAvatar = document.getElementById('profile-avatar-display');
    const initial = document.getElementById('user-avatar-initial');
    if (!profileAvatar) return;

    if (data.avatar_url) {
        profileAvatar.style.backgroundImage = `url(${API_BASE_URL}${data.avatar_url})`;
        profileAvatar.style.backgroundSize = 'cover';
        profileAvatar.style.backgroundPosition = 'center';
        if (initial) initial.style.display = 'none';
    } else {
        if (initial && data.name) {
            initial.textContent = data.name[0].toUpperCase();
            initial.style.display = '';
        }
    }
}

async function handleAvatarUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    // Show loading spinner
    const loadingOverlay = document.getElementById('avatar-loading');
    if (loadingOverlay) {
        loadingOverlay.style.opacity = '1';
        loadingOverlay.style.pointerEvents = 'auto';
    }

    const formData = new FormData();
    formData.append('avatar', file);

    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/auth/avatar`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
                // Do NOT set Content-Type here — the browser sets it automatically with multipart boundary
            },
            body: formData
        });

        if (response.status === 401 || response.status === 403) {
            localStorage.removeItem('token');
            window.location.replace('login.html');
            return;
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
            throw new Error(error.detail || 'Upload failed');
        }

        const data = await response.json();

        // Update profile avatar immediately
        applyAvatarToProfilePage({ avatar_url: data.avatar_url });

        // Also update any header avatars
        if (typeof loadMeAndApplyAvatar === 'function') {
            loadMeAndApplyAvatar();
        }

    } catch (err) {
        alert('Upload failed: ' + err.message);
    } finally {
        // Hide spinner
        if (loadingOverlay) {
            loadingOverlay.style.opacity = '0';
            loadingOverlay.style.pointerEvents = 'none';
        }
        // Clear input so same file can be re-uploaded
        e.target.value = '';
    }
}

function handleLogout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

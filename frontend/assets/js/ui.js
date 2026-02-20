async function loadMeAndApplyAvatar() {
    try {
        const data = await apiFetch('/auth/me');
        const initial = data.name ? data.name[0].toUpperCase() : '?';

        // Update all HEADER avatar elements (small circles in nav bar)
        // This deliberately skips the large profile-avatar-display (handled by profile.js)
        const avatars = document.querySelectorAll('.js-avatar');
        avatars.forEach(avatar => {
            if (data.avatar_url) {
                avatar.innerHTML = `<img src="${API_BASE_URL}${data.avatar_url}" class="w-full h-full object-cover" alt="${data.name}" style="border-radius:inherit;">`;
            } else {
                avatar.innerHTML = `<span class="font-bold text-sm text-primary">${initial}</span>`;
            }
        });

        return data;
    } catch (err) {
        console.error('Failed to load global user data:', err);
    }
}

// Auto-load on DOMContentLoaded
document.addEventListener('DOMContentLoaded', loadMeAndApplyAvatar);

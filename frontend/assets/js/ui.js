async function loadMeAndApplyAvatar() {
    try {
        const data = await apiFetch('/auth/me');
        const initial = data.name ? data.name[0].toUpperCase() : '?';

        // Update all HEADER avatar elements (small circles in nav bar)
        // This deliberately skips the large profile-avatar-display (handled by profile.js)
        const avatars = document.querySelectorAll('.js-avatar');
        avatars.forEach(avatar => {
            if (data.avatar_url) {
                // Avatars are now served from Cloudflare Assets as .webp
                // Original avatar_url is /static/avatars/{id}.{ext}
                // We want {ASSETS_BASE_URL}/assets/avatars/{id}.webp
                const avatarId = data.avatar_url.split('/').pop().split('.')[0];
                const cloudflareAvatarUrl = `${ASSETS_BASE_URL}/assets/avatars/${avatarId}.webp`;

                // Top nav avatars should NOT be lazy loaded
                avatar.innerHTML = `<img src="${cloudflareAvatarUrl}" 
                    class="w-full h-full object-cover" 
                    alt="${data.name}" 
                    width="40" height="40"
                    style="border-radius:inherit;">`;
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

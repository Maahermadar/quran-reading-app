async function loadMeAndApplyAvatar() {
    try {
        const data = await apiFetch('/auth/me');
        const initial = data.name ? data.name[0].toUpperCase() : '?';

        // Update all HEADER avatar elements (small circles in nav bar)
        // This deliberately skips the large profile-avatar-display (handled by profile.js)
        const avatars = document.querySelectorAll('.js-avatar');
        avatars.forEach(avatar => {
            if (data.avatar_url) {
                const cloudflareAvatarUrl = getAvatarUrl(data.avatar_url);

                // Top nav avatars should NOT be lazy loaded
                // Added smart fallback: if Cloudflare 404s (e.g. just after upload), try local backend
                const localFallback = `${API_BASE_URL}${data.avatar_url}`;
                avatar.innerHTML = `<img src="${cloudflareAvatarUrl}" 
                    class="w-full h-full object-cover" 
                    alt="${data.name}" 
                    width="40" height="40"
                    style="border-radius:inherit;"
                    onerror="this.onerror=null; this.src='${localFallback}';">`;
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

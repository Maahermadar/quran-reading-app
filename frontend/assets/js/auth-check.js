// Auth Guard — must be loaded as the first script on protected app pages.
// Immediately redirects unauthenticated users to the login page.
(function () {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.replace('login.html');
        return;
    }

    // Auth Gate: Hide main content until UI scripts are ready
    // We add a style tag to hide the body initially to prevent flash of unstyled/placeholder content
    const style = document.createElement('style');
    style.id = 'auth-gate-style';
    style.innerHTML = `
        body { transition: opacity 0.3s ease; }
    `;
    document.head.appendChild(style);

    // If we have a cached user, we can show the UI faster
    // This will be handled by individual page scripts calling document.body.classList.add('auth-ready')
})();

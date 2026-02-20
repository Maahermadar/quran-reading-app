// Auth Guard — must be loaded as the first script on protected app pages.
// Immediately redirects unauthenticated users to the login page.
(function () {
    const token = localStorage.getItem('token');
    if (!token) {
        // Determine the correct path to login.html relative to the current page
        window.location.replace('login.html');
    }
})();

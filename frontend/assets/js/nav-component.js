/**
 * nav-component.js
 * Standardized bottom navigation for the Quran reading App
 */

function renderBottomNav() {
    const navContainer = document.createElement('nav');
    navContainer.className = "fixed bottom-0 left-0 right-0 bg-white/90 dark:bg-slate-900/90 backdrop-blur-lg border-t border-slate-200 dark:border-slate-800 px-6 pb-6 pt-3 z-50";

    const navItems = [
        { name: 'HOME', icon: 'home', link: 'home.html' },
        { name: 'INSIGHTS', icon: 'bar_chart', link: 'insights.html' },
        { name: 'TIPS', icon: 'lightbulb', link: 'tips.html' },
        { name: 'PROFILE', icon: 'person', link: 'profile.html' }
    ];

    const navContent = `
        <div class="flex items-center justify-between max-w-md mx-auto relative px-2">
            ${navItems.map(item => {
        const currentPath = window.location.pathname;
        // Robust path matching: handles root, .html extensions, and subfolders
        const isActive = currentPath.includes(item.link) ||
            (currentPath.endsWith('/') && item.link === 'home.html') ||
            (currentPath === '' && item.link === 'home.html');

        const activeClass = isActive
            ? 'text-emerald-700 dark:text-emerald-400'
            : 'text-slate-400 hover:text-primary transition-all duration-300';

        const iconFill = isActive ? "'FILL' 1, 'wght' 700" : "'FILL' 0, 'wght' 400";

        return `
                    <a class="flex flex-col items-center gap-1.5 py-1 px-4 rounded-2xl relative transition-all duration-300 ${isActive ? 'bg-emerald-50 dark:bg-emerald-900/20' : ''} ${activeClass}" href="${item.link}">
                        <div class="relative flex items-center justify-center">
                            <span class="material-symbols-outlined text-[24px]" style="font-variation-settings: ${iconFill}">${item.icon}</span>
                            ${isActive ? '<div class="absolute -top-1 -right-1 w-1.5 h-1.5 bg-emerald-600 rounded-full shadow-[0_0_8px_rgba(5,150,105,0.5)]"></div>' : ''}
                        </div>
                        <span class="text-[9px] ${isActive ? 'font-black' : 'font-bold'} tracking-widest uppercase transition-all overflow-hidden whitespace-nowrap">${item.name}</span>
                    </a>
                `;
    }).join('')}
        </div>
    `;

    navContainer.innerHTML = navContent;
    document.body.appendChild(navContainer);

    // Pre-fetch navigation links on hover/touch
    navContainer.querySelectorAll('a').forEach(link => {
        const prefetch = () => {
            const href = link.getAttribute('href');
            if (href && !window.location.pathname.includes(href)) {
                const linkTag = document.createElement('link');
                linkTag.rel = 'prefetch';
                linkTag.href = href;
                document.head.appendChild(linkTag);
                // Only prefetch once per link
                link.removeEventListener('mouseenter', prefetch);
                link.removeEventListener('touchstart', prefetch);
            }
        };
        link.addEventListener('mouseenter', prefetch, { passive: true });
        link.addEventListener('touchstart', prefetch, { passive: true });
    });
}

// Ensure DOM is loaded before rendering
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderBottomNav);
} else {
    renderBottomNav();
}

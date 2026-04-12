/**
 * theme_helpers.js - Handles granular forensic skin transitions (v1.46.03).
 */

function initTheme() {
    const config = window.CONFIG?.themes;
    const defaultTheme = config?.active || 'forensic_dark';
    const savedTheme = localStorage.getItem('mwv_theme') || defaultTheme;
    setTheme(savedTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('mwv_theme', theme);
    console.info(`[Theme-Engine] Active Skin: ${theme.toUpperCase()}`);
    
    // Notify components of theme change
    if (typeof mwv_trace === 'function') {
        mwv_trace('THEME-SWITCH', theme);
    }
}

function toggleTheme() {
    const config = window.CONFIG?.themes;
    if (!config || !config.available) {
        // Fallback legacy toggle
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = (currentTheme === 'dark' || currentTheme === 'forensic_dark') ? 'light_pro' : 'forensic_dark';
        setTheme(newTheme);
        return;
    }
    
    const current = document.documentElement.getAttribute('data-theme') || config.active;
    const currentIndex = config.available.indexOf(current);
    const nextIndex = (currentIndex + 1) % config.available.length;
    const nextTheme = config.available[nextIndex];
    
    setTheme(nextTheme);
    if (typeof showToast === 'function') showToast(`Theme: ${nextTheme}`, 1500);
}

// Auto-init on load
document.addEventListener('DOMContentLoaded', initTheme);

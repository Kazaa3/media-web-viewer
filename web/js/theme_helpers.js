/**
 * theme_helpers.js - Handles light/dark mode transitions and persistence.
 */

function initTheme() {
    const savedTheme = localStorage.getItem('mwv_theme') || 'light';
    setTheme(savedTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('mwv_theme', theme);
    
    // Update toggle icons if any
    const sunIcon = document.getElementById('theme-icon-sun');
    const moonIcon = document.getElementById('theme-icon-moon');
    
    if (sunIcon && moonIcon) {
        sunIcon.style.display = (theme === 'dark') ? 'none' : 'block';
        moonIcon.style.display = (theme === 'dark') ? 'block' : 'none';
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
    setTheme(newTheme);
}

// Auto-init on load
document.addEventListener('DOMContentLoaded', initTheme);

// Created with MWV v1.46.00-MASTER

/**
 * UI Translations Dictionary & Orchestrator
 * Enhanced logic for asynchronous i18n.json fetching and attribute translation.
 */

let currentLanguage = 'de';
let translations = {};

/**
 * Initializes translations from the local i18n.json file.
 */
async function initTranslations() {
    try {
        const response = await fetch('i18n.json');
        translations = await response.json();
        
        if (typeof eel !== 'undefined' && typeof eel.get_language === 'function') {
            currentLanguage = await eel.get_language()();
        }

        if (typeof currentLanguage !== 'string' || !translations[currentLanguage]) {
            currentLanguage = 'de';
        }

        const select = document.getElementById('language-select');
        if (select) select.value = currentLanguage;

        applyTranslations(currentLanguage);

        if (typeof checkConnection === 'function') checkConnection();
        if (typeof syncVersionInfo === 'function') syncVersionInfo();

        const activeTab = localStorage.getItem('mwv_active_tab') || 'player';
        if (typeof switchTab === 'function') {
            const btn = document.querySelector(`.tab-btn[onclick*="'${activeTab}'"]`);
            switchTab(activeTab, btn);
        }
    } catch (e) {
        console.error('[i18n] Failed to load translations:', e);
        if (typeof showToast === 'function') {
            showToast('Critical Boot Error: ' + e.message, 5000);
        }
    }
}

/**
 * Applies translations to all elements with data-i18n attributes.
 */
function applyTranslations(lang) {
    currentLanguage = lang;
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        let val = null;

        // Handle [attribute]key format
        const attrMatch = key.match(/^\[([^\]]+)\](.+)$/);
        if (attrMatch) {
            const attr = attrMatch[1];
            const subKey = attrMatch[2];
            val = t(subKey);
            if (typeof val === 'string') {
                el.setAttribute(attr, val);
            }
            return;
        }

        val = t(key);
        if (val === key || typeof val !== 'string') return;

        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = val;
        } else {
            if (el.children.length === 0) {
                el.innerHTML = val;
            }
        }
    });
    document.documentElement.lang = lang;
}

/**
 * Changes the application language and persists it via the backend.
 */
async function changeLanguage(lang) {
    if (typeof eel !== 'undefined' && typeof eel.set_language === 'function') {
        await eel.set_language(lang)();
    }
    applyTranslations(lang);
    
    // Refresh library after language change to update specific badges
    if (typeof renderLibrary === 'function') renderLibrary();
}

/**
 * Translation helper for functional usage.
 */
function t(key, defaultValue) {
    if (translations[currentLanguage] && translations[currentLanguage][key]) {
        return translations[currentLanguage][key].replace(/\\n/g, '\n');
    }
    if (translations.de && translations.de[key]) {
        return translations.de[key].replace(/\\n/g, '\n');
    }
    return defaultValue || key;
}

// Global initialization
window.addEventListener('load', initTranslations);

// Created with MWV v1.46.00-MASTER

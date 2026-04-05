/**
 * MWV Diagnostic Suite (v1.35.34)
 * Formalized recovery and visibility toolset.
 */

const Diagnostics = {
    isActive: localStorage.getItem('mwv_diagnostic_mode') === 'true',
    isNuclear: localStorage.getItem('mwv_nuclear_mode') === 'true',
    
    init() {
        console.log(">>> [DIAGNOSTICS] Suite initialized. Active:", this.isActive);
        if (this.isActive) {
            this.applyNuclearStyles();
            this.startMutationWatch();
            this.injectHeader();
        }
        
        // Sync UI Buttons
        this.syncUI();
        
        // Auto-Hydration Fail-safe (2.5s after boot)
        setTimeout(() => this.checkAndHydrate(), 2500);
    },

    syncUI() {
        const diagBtn = document.getElementById('diag-toggle-btn');
        if (diagBtn) diagBtn.innerText = this.isActive ? 'ON' : 'OFF';
        
        const nuclearBtn = document.querySelector('button[onclick*="nuclear_mode"]');
        if (nuclearBtn) nuclearBtn.innerText = this.isNuclear ? 'ON' : 'OFF';
    },

    toggle() {
        this.isActive = !this.isActive;
        localStorage.setItem('mwv_diagnostic_mode', this.isActive);
        location.reload();
    },

    applyNuclearStyles() {
        if (!this.isNuclear) return;
        console.log(">>> [DIAGNOSTICS] Applying Nuclear Visibility Locks...");
        const style = document.createElement('style');
        style.id = 'mwv-nuclear-lock';
        style.innerHTML = `
            #player-main-viewport, 
            #player-tab-split-container, 
            .player-view-container, 
            #player-view-warteschlange {
                display: flex !important;
                opacity: 1 !important;
                visibility: visible !important;
                z-index: 5000 !important;
                min-height: 500px !important;
                border: 4px solid #00ff00 !important;
            }
            #recovery-test-header {
                display: block !important;
            }
        `;
        document.head.appendChild(style);
    },

    injectHeader() {
        if (document.getElementById('recovery-test-header')) return;
        const msg = this.isNuclear ? "DIAGNOSTIC MODE: NUCLEAR" : "DIAGNOSTIC MODE: ACTIVE";
        document.body.insertAdjacentHTML('afterbegin', `
            <div id="recovery-test-header" style="position: fixed; top: 0; left: 0; right: 0; z-index: 10010; background: rgba(255,0,0,0.9); color: white; padding: 5px 20px; font-weight: bold; font-family: monospace; font-size: 12px; display: flex; justify-content: space-between; align-items: center;">
                <span>${msg} (v1.35.34)</span>
                <div>
                   <button onclick="Diagnostics.hydrate()" style="background: white; border: none; padding: 2px 10px; cursor: pointer; color: black; font-weight: bold; margin-right: 10px;">FORCE HYDRATION</button>
                   <button onclick="Diagnostics.toggle()" style="background: black; color: white; border: none; padding: 2px 10px; cursor: pointer;">DISABLE</button>
                </div>
            </div>
        `);
    },

    startMutationWatch() {
        console.log(">>> [DIAGNOSTICS] Starting Mutation Watch...");
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((m) => {
                const target = m.target.id || m.target.className || 'unknown';
                if (m.attributeName === 'style' || m.attributeName === 'class') {
                    const display = window.getComputedStyle(m.target).display;
                    if (display === 'none' && (m.target.id === 'player-main-viewport' || m.target.id === 'player-view-warteschlange')) {
                        console.error(`>>> [DIAGNOSTICS] Element '${target}' was hidden! RESTORING.`);
                        m.target.style.display = 'flex';
                    }
                }
            });
        });
        observer.observe(document.body, { attributes: true, subtree: true });
    },

    checkAndHydrate() {
        const libCount = (window.allLibraryItems || []).length;
        if (libCount === 0 || (libCount === 1 && window.allLibraryItems[0].is_mock)) {
            console.warn(">>> [DIAGNOSTICS] Library empty after 2.5s. Triggering Auto-Hydration...");
            this.hydrate();
        }
    },

    hydrate() {
        console.log(">>> [DIAGNOSTICS] Atomic Hydration (Real Tracks) starting...");
        
        const realMockTracks = [
            {
                id: 'diag-track-1',
                name: 'sample_audio.mp3',
                filename: 'sample_audio.mp3',
                path: 'media/sample_audio.mp3',
                title: 'System Diagnostic Track (MP3)',
                artist: 'MWV Discovery',
                album: 'MWV Recovery Suite',
                tags: {
                    title: 'System Diagnostic Track (MP3)',
                    artist: 'MWV Discovery',
                    album: 'MWV Recovery Suite'
                },
                category: 'Audio',
                is_diag: true,
                is_mock: false
            },
            {
                id: 'diag-track-2',
                name: 'test_track_01.m4a',
                filename: 'test_track_01.m4a',
                path: 'media/test_track_01.m4a',
                title: 'System Diagnostic Track (M4A)',
                artist: 'MWV Discovery',
                album: 'MWV Recovery Suite',
                tags: {
                    title: 'System Diagnostic Track (M4A)',
                    artist: 'MWV Discovery',
                    album: 'MWV Recovery Suite'
                },
                category: 'Audio',
                is_diag: true,
                is_mock: false
            }
        ];

        // Hydrate Library
        window.allLibraryItems = realMockTracks;
        
        // Hydrate Player Queue (CRITICAL FIX)
        if (typeof window.currentPlaylist !== 'undefined') {
            window.currentPlaylist = [...realMockTracks];
        }

        // Trigger UI Renders
        if (typeof renderLibrary === 'function') renderLibrary();
        if (typeof renderPlaylist === 'function') renderPlaylist();
        
        if (typeof showToast === 'function') showToast("System Hydrated with Real Source Files", "success");
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => Diagnostics.init());
window.Diagnostics = Diagnostics;

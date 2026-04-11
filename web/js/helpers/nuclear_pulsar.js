/**
 * Nuclear Pulsar Recovery Engine (v1.46.03)
 * Centralized logic for forcing fragment injections and DOM visibility.
 */
const ForensicRecovery = {
    /**
     * Forces a fragment injection into a target container.
     * @param {string} targetId - The DOM ID of the container.
     * @param {string} fragmentPath - The path to the HTML fragment.
     */
    async forceForensicInjection(targetId, fragmentPath) {
        console.warn(`[PULSAR] Forcing Injection: ${targetId} <- ${fragmentPath}`);
        const container = document.getElementById(targetId);
        if (!container) {
            console.error(`[PULSAR] Target container ${targetId} NOT FOUND.`);
            return;
        }

        try {
            const response = await fetch(fragmentPath);
            if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
            const html = await response.text();
            
            // Clean container and inject
            container.innerHTML = html;
            
            // Re-execute scripts manually since innerHTML doesn't run scripts
            const scripts = container.querySelectorAll('script');
            scripts.forEach(oldScript => {
                const newScript = document.createElement('script');
                Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });

            console.info(`[PULSAR] Injection Successful: ${targetId}`);
            
            // LOG TO BACKEND
            if (typeof eel !== 'undefined' && eel.log_spawn_event) {
                eel.log_spawn_event(targetId, "hydrated");
            }

        } catch (err) {
            console.error(`[PULSAR] Injection FAILED for ${targetId}:`, err);
            if (typeof eel !== 'undefined' && eel.log_spawn_event) {
                eel.log_spawn_event(targetId, `failed: ${err.message}`);
            }
        }
    },

    /**
     * Brute-force visibility pulse.
     */
    triggerNuclearPulsar() {
        console.warn("☢️ [PULSAR] NUCLEAR VISIBILITY TRIGGERED.");
        document.querySelectorAll('.tab-content, .deck-view, .recovery-placeholder').forEach(el => {
            el.style.display = 'flex';
            el.style.visibility = 'visible';
            el.style.opacity = '1';
            el.style.zIndex = '9999';
        });
    }
};

// Global Exposure
window.ForensicRecovery = ForensicRecovery;
window.triggerNuclearPulsar = ForensicRecovery.triggerNuclearPulsar;

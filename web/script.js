async function loadMedia() {
    try {
        const result = await eel.scan_media()();
        const list = document.getElementById("media-list");
        list.innerHTML = "";

        for (const item of result.media) {
            const li = document.createElement("li");
            li.textContent = item.name;
            list.appendChild(li);
        }
    } catch (e) {
        alert("Fehler: " + e.message);
    }
}

// Populate default folder input from backend and wire Browse button (including debug controls)
async function initDefaultFolder() {
    try {
        const dir = await eel.get_default_media_dir()();
        const input = document.getElementById("default-folder-input");
        const inputDebug = document.getElementById("default-folder-input-debug");
        if (input) input.value = dir;
        if (inputDebug) inputDebug.value = dir;

        const btn = document.getElementById("browse-folder-btn");
        if (btn) {
            btn.addEventListener('click', async () => {
                const d = document.getElementById("default-folder-input").value || null;
                try {
                    const res = await eel.browse_dir(d)();
                    // Display in browser-tab textarea
                    const out = document.getElementById('browse-results');
                    if (res.error) {
                        if (out) out.value = `# Fehler: ${res.error}`;
                        else alert(res.error);
                    } else {
                        if (out) {
                            const lines = [];
                            if (res.items && res.items.length > 0) {
                                for (const it of res.items) {
                                    lines.push(`# ${it.name} [${it.type}] ${it.size ? '('+it.size+')' : ''}`);
                                }
                            } else {
                                lines.push('# Kein Inhalt im Verzeichnis');
                            }
                            out.value = lines.join('\n');
                        } else {
                            console.log('browse_dir result:', res);
                        }
                    }
                } catch (e) {
                    alert('Fehler beim Durchsuchen: ' + e.message);
                }
            });
        }

        const btnDbg = document.getElementById("browse-folder-btn-debug");
        if (btnDbg) {
            btnDbg.addEventListener('click', async () => {
                const d = document.getElementById("default-folder-input-debug").value || null;
                try {
                    const res = await eel.browse_dir(d)();
                    const out = document.getElementById('browse-results-debug');
                    if (res.error) {
                        if (out) out.value = `# Fehler: ${res.error}`;
                    } else {
                        if (out) {
                            const lines = [];
                            if (res.items && res.items.length > 0) {
                                for (const it of res.items) {
                                    lines.push(`# ${it.name} [${it.type}] ${it.size ? '('+it.size+')' : ''}`);
                                }
                            } else {
                                lines.push('# Kein Inhalt im Verzeichnis');
                            }
                            out.value = lines.join('\n');
                        }
                    }
                } catch (e) {
                    const out = document.getElementById('browse-results-debug');
                    if (out) out.value = `# Fehler beim Durchsuchen: ${e.message}`;
                }
            });
        }

        const scanDbg = document.getElementById('scan-btn-debug');
        if (scanDbg) scanDbg.addEventListener('click', () => scan());
    } catch (e) {
        console.error('Could not get default media dir:', e);
    }
}

window.addEventListener('DOMContentLoaded', function() {
    initDefaultFolder();
});

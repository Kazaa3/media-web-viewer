function isUnsupportedMediaError(reason) {
            const text = String(reason || '');
            return text.includes('NotSupportedError') || text.includes('no supported source was found');
        }

        window.onerror = function (msg, url, lineNo, columnNo, error) {
            alert("JS Error: " + msg + "\nLine: " + lineNo + "\nCol: " + columnNo);
            return false;
        };
        window.addEventListener('unhandledrejection', function (event) {
            if (isUnsupportedMediaError(event.reason)) {
                console.warn('Unsupported media source rejected by browser:', event.reason);
                const statusEl = document.getElementById('active-orchestration-status-message-renderer');
                if (statusEl) {
                    statusEl.textContent = t('player_unsupported_source') || 'Unsupported media source for browser playback.';
                }
                event.preventDefault();
                return;
            }
            console.error("Uncaught Promise: ", event.reason);
        });
/**
 * Metadata Editor Helpers
 * Extracted from app.html to improve modularity and avoid line-number drift.
 */

/**
 * Saves modified tags to the database and optionally to the file.
 */
async function saveTags() {
    const itemName = readValue('edit-item-name');
    if (!itemName) return;

    const tags = {};
    document.querySelectorAll('#edit-dynamic-tags .tag-input').forEach(input => {
        tags[input.dataset.tag] = input.value;
    });

    if (typeof appendUiTrace === 'function') appendUiTrace(`[Edit] Saving tags for ${itemName}...`);
    try {
        const res = await eel.save_metadata(itemName, tags)();
        if (res && res.status === 'ok') {
            if (typeof showToast === 'function') showToast("Tags erfolgreich in DB gespeichert", "success");
            if (typeof refreshLibrary === 'function') refreshLibrary();
        } else {
            if (typeof showToast === 'function') showToast("Fehler beim Speichern: " + (res.message || 'unknown'), "error");
        }
    } catch (err) {
        console.error("Error saving tags:", err);
    }
}

/**
 * Renames a media file on the filesystem and updates the database.
 */
async function renameMedia() {
    const itemName = readValue('edit-item-name');
    if (!itemName) return;

    const newName = prompt("Neuer Dateiname (ohne Pfad):", itemName.split('/').pop());
    if (!newName || newName === itemName.split('/').pop()) return;

    if (typeof appendUiTrace === 'function') appendUiTrace(`[Edit] Renaming ${itemName} to ${newName}...`);
    try {
        const res = await eel.rename_media(itemName, newName)();
        if (res && res.status === 'ok') {
            if (typeof showToast === 'function') showToast("Datei erfolgreich umbenannt", "success");
            safeValue('edit-item-name', res.new_path);
            safeText('edit-filename-display', res.new_path);
            if (typeof refreshLibrary === 'function') refreshLibrary();
        } else {
            alert("Fehler beim Umbenennen: " + (res ? res.message : 'unbekannt'));
        }
    } catch (err) {
        console.error("Error renaming media:", err);
    }
}

/**
 * Deletes a media file from the database and potentially the disk.
 */
async function deleteMediaFromEdit() {
    const itemName = readValue('edit-item-name');
    if (!itemName) return;

    if (!confirm(`Möchtest du '${itemName}' wirklich aus der Datenbank löschen?`)) return;

    if (typeof appendUiTrace === 'function') appendUiTrace(`[Edit] Deleting ${itemName}...`);
    try {
        const res = await eel.delete_media(itemName)();
        if (res && res.status === 'ok') {
            if (typeof showToast === 'function') showToast("Datei aus Datenbank entfernt", "info");
            resetEditForm();
            if (typeof refreshLibrary === 'function') refreshLibrary();
        } else {
            alert("Fehler beim Löschen: " + (res ? res.message : 'unbekannt'));
        }
    } catch (err) {
        console.error("Error deleting media:", err);
    }
}

/**
 * Triggers an ISBN scan to fetch book metadata.
 */
async function triggerIsbnScan() {
    const isbn = readValue('isbn-scanner-input');
    if (!isbn) {
        if (typeof showToast === 'function') showToast("Bitte ISBN eingeben", "warning");
        return;
    }

    if (typeof appendUiTrace === 'function') appendUiTrace(`[Edit] Scanning ISBN: ${isbn}...`);
    try {
        const res = await eel.trigger_isbn_scan(isbn)();
        if (res && res.status === 'success') {
            if (typeof showToast === 'function') showToast("ISBN Metadaten geladen", "success");
            // Fill form with results
            if (res.metadata) {
                for (const [key, val] of Object.entries(res.metadata)) {
                    const input = document.querySelector(`.tag-input[data-tag="${key}"]`);
                    if (input) input.value = val;
                }
            }
        } else {
            if (typeof showToast === 'function') showToast("Fehler beim ISBN-Scan: " + (res.message || 'not found'), "error");
        }
    } catch (err) {
        console.error("Error in ISBN scan:", err);
    }
}

/**
 * Resets the metadata editor form.
 */
function resetEditForm() {
    safeValue('edit-item-name', '');
    safeText('edit-filename-display', '-');
    safeStyle('edit-cover', 'src', '');
    document.getElementById('edit-dynamic-tags').innerHTML = '';
}

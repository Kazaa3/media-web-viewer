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
    if (typeof safeStyle === 'function') {
        safeStyle('edit-placeholder', 'display', 'flex');
        safeStyle('edit-form-container', 'display', 'none');
    }
    if (typeof safeValue === 'function') safeValue('edit-item-name', '');
    if (typeof safeText === 'function') safeText('edit-filename-display', '-');
    const cover = document.getElementById('edit-cover');
    if (cover) cover.src = '';
    const dynTags = document.getElementById('edit-dynamic-tags');
    if (dynTags) dynTags.innerHTML = '';
}

/**
 * Opens the edit form for a specific media item.
 */
function openEditForm(item) {
    console.log("[Editor] Opening form for:", item.name);
    if (typeof safeStyle === 'function') {
        safeStyle('edit-placeholder', 'display', 'none', 'important');
        safeStyle('edit-form-container', 'display', 'block', 'important');
    }

    if (!item) {
        console.error("[Editor] No item provided!");
        return;
    }

    if (typeof safeValue === 'function') safeValue('edit-item-name', item.name);
    if (typeof safeText === 'function') safeText('edit-filename-display', item.name);
    
    const cover = document.getElementById('edit-cover');
    if (cover) cover.src = `/cover/${encodeURIComponent(item.name)}`;

    const container = document.getElementById('edit-dynamic-tags');
    if (container) container.innerHTML = '';

    // Alphabetically sort for order + ensure core fields
    let keys = Object.keys(item.tags).sort();
    const coreKeys = ['title', 'artist', 'album', 'year', 'genre', 'isbn', 'imdb', 'tmdb', 'discogs'];
    coreKeys.forEach(k => {
        if (!keys.includes(k)) keys.push(k);
    });
    keys.sort();

    keys.forEach(key => {
        if (key === 'chapters' || key === '_parser_times') return;

        const row = document.createElement('div');
        row.style.display = 'flex';
        row.style.alignItems = 'center';
        row.style.padding = '8px 0';
        row.style.borderBottom = '1px solid #f9f9f9';

        const label = document.createElement('label');
        label.style.width = '140px';
        label.style.fontSize = '0.85em';
        label.style.color = '#666';
        label.style.textTransform = 'capitalize';
        label.innerText = key.replace('_', ' ');

        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'edit-dynamic-input';
        input.dataset.key = key;
        input.value = item.tags[key] || '';
        input.style.flex = '1';
        input.style.padding = '8px 12px';
        input.style.border = '1px solid #eee';
        input.style.borderRadius = '4px';
        input.style.fontSize = '0.95em';
        input.onfocus = () => input.style.borderColor = '#2a7';
        input.onblur = () => input.style.borderColor = '#eee';

        row.appendChild(label);
        row.appendChild(input);
        if (container) container.appendChild(row);
    });

    if (item.tags.chapters && Array.isArray(item.tags.chapters) && item.tags.chapters.length > 0) {
        const chapHeader = document.createElement('h4');
        chapHeader.innerText = 'Kapitel bearbeiten';
        chapHeader.style.marginTop = '20px';
        chapHeader.style.marginBottom = '10px';
        chapHeader.style.color = '#555';
        if (container) container.appendChild(chapHeader);

        item.tags.chapters.forEach((chap, idx) => {
            const row = document.createElement('div');
            row.style.display = 'flex';
            row.style.alignItems = 'center';
            row.style.padding = '4px 0';

            const label = document.createElement('label');
            label.style.width = '140px';
            label.style.fontSize = '0.85em';
            label.style.color = '#888';
            label.innerText = `Kapitel ${idx + 1}`;

            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'edit-chapter-input';
            input.dataset.index = idx;
            input.value = chap.title || `Kapitel ${idx + 1}`;
            input.style.flex = '1';
            input.style.padding = '6px 12px';
            input.style.border = '1px solid #eee';
            input.style.borderRadius = '4px';
            input.style.fontSize = '0.9em';
            input.style.background = '#fafafa';

            row.appendChild(label);
            row.appendChild(input);
            if (container) container.appendChild(row);
        });
    }
}

/**
 * Saves modified tags directly to the physical file.
 */
async function saveToFileUI(event) {
    const name = readValue('edit-item-name');
    if (!name) {
        alert(t('edit_no_selection_error') || 'No selection');
        return;
    }

    const tags = {};
    const tagRows = document.querySelectorAll('.edit-tag-row');
    tagRows.forEach(row => {
        const keyEl = row.querySelector('.tag-key');
        const valEl = row.querySelector('.tag-val');
        if (keyEl && valEl) {
            const key = keyEl.innerText.replace(':', '').trim().toLowerCase();
            tags[key] = valEl.value;
        }
    });

    // Button context
    const btn = event.currentTarget;
    const originalBtnText = btn.innerHTML;
    btn.innerHTML = (t('edit_saving') || 'Speichern...') + ' <svg width="12" height="12"><use href="#icon-clock"></use></svg>';
    btn.disabled = true;

    try {
        const result = await eel.save_tags_to_file(name, tags)();
        if (result.success) {
            alert(t('edit_save_to_file_success') || 'Erfolgreich in Datei gespeichert!');
            if (typeof loadLibrary === 'function') loadLibrary(); 
        } else {
            alert((t('edit_save_to_file_error') || 'Fehler beim Speichern in Datei: ') + result.error);
        }
    } catch (e) {
        alert('Eel error: ' + e);
    } finally {
        btn.innerHTML = originalBtnText;
        btn.disabled = false;
    }
}

function jumpToEdit(item) {
    const editBtn = document.querySelector('button[onclick*="\'edit\'"]');
    if (typeof switchTab === 'function') switchTab('edit', editBtn);
    openEditForm(item);
}

// Created with MWV v1.45.100-EVO-REBUILD

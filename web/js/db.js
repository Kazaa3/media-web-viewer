/**
 * db.js
 * Low-level database utility module for backend communication.
 * Handles fetching, scanning, and metadata persistence.
 */

/**
 * Fetches the entire library from the backend.
 */
async function getLibrary() {
    if (typeof mwv_trace_render === 'function') mwv_trace_render('DB-EEL', 'CALL-START');
    if (typeof eel === 'undefined') return { media: [] };

    // Wait for eel.get_library to be exposed (up to 2s)
    let attempts = 0;
    const maxAttempts = 4; // 4 x 500ms = 2s
    while (typeof eel.get_library !== 'function' && attempts < maxAttempts) {
        console.warn(`[DB] get_library: Eel not ready yet (Attempt ${attempts+1}/${maxAttempts})...`);
        await new Promise(resolve => setTimeout(resolve, 500));
        attempts++;
    }

    if (typeof eel.get_library !== 'function') {
        if (typeof mwv_trace_render === 'function') mwv_trace_render('DB-EEL', 'TIMEOUT');
        console.error("[DB] get_library: Eel exposure failed or timed out.");
        return { media: [] };
    }

    try {
        return await eel.get_library()();
    } catch (e) {
        console.error("[DB] Error fetching library:", e);
        return { media: [] };
    }
}

/**
 * Fetches filtered library items.
 */
async function getLibraryFiltered(search = "", genre = "all", year = "all", sortBy = "name") {
    if (typeof eel === 'undefined') return { media: [] };
    try {
        return await eel.get_library_filtered(search, genre, year, sortBy)();
    } catch (e) {
        console.error("[DB] Error fetching filtered library:", e);
        return { media: [] };
    }
}

/**
 * Initiates a backend media scan.
 */
async function scanMedia(dirPath = null, clearDb = true) {
    if (typeof eel === 'undefined') return;
    try {
        if (typeof appendUiTrace === 'function') appendUiTrace(`[DB] Initiating scan for: ${dirPath || "all"} (clearDb: ${clearDb})`);
        return await eel.scan_media(dirPath, clearDb)();
    } catch (e) {
        console.error("[DB] Error initiating scan:", e);
    }
}

/**
 * Adds a single file to the library.
 */
async function addFileToLibrary(path) {
    if (typeof eel === 'undefined' || !path) return { status: 'error' };
    try {
        return await eel.add_file_to_library(path)();
    } catch (e) {
        console.error("[DB] Error adding file:", e);
        return { status: 'error' };
    }
}

/**
 * Saves metadata for a specific item.
 */
async function saveMetadata(itemName, tags) {
    if (typeof eel === 'undefined') return { status: 'error' };
    try {
        return await eel.save_metadata(itemName, tags)();
    } catch (e) {
        console.error("[DB] Error saving metadata:", e);
        return { status: 'error' };
    }
}

/**
 * Fetches library folder configuration.
 */
async function getLibraryFolders() {
    if (typeof eel === 'undefined') return [];
    try {
        return await eel.get_library_folders()();
    } catch (e) {
        console.error("[DB] Error fetching folders:", e);
        return [];
    }
}

/**
 * db.js
 * Low-level database utility module for backend communication.
 * Handles fetching, scanning, and metadata persistence.
 */

/**
 * Fetches the entire library from the backend.
 */
async function getLibrary(auditStage = 0) {
    if (typeof mwv_trace_render === 'function') mwv_trace_render('DB-EEL', `CALL-START (Stage: ${auditStage})`);
    if (typeof eel === 'undefined') return { media: [] };
    
    // Auto-fallback for stage names
    const forceRaw = (auditStage === 2);

    try {
        console.info(`[DB] getLibrary Request: Stage=${auditStage}, ForceRaw=${forceRaw}`);
        const result = await eel.get_library(forceRaw, auditStage)();
        console.log(`[DB] getLibrary Response:`, result);
        return result;
    } catch (e) {
        console.error("[DB] Error fetching library:", e);
        return { media: [], status: "error" };
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

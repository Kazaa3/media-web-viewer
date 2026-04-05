console.log(">>> [RECOVERY] Injecting test header...");
document.body.insertAdjacentHTML('afterbegin', '<h1 id="recovery-test-header" style="color: red; position: fixed; top: 10px; left: 10px; z-index: 9999; background: white; padding: 10px; border: 5px solid red;">RECOVERY SUCCESS (v1.35.6)</h1>');
if (typeof allLibraryItems !== 'undefined') {
    console.log(">>> [RECOVERY] allLibraryItems exists. Count:", allLibraryItems.length);
} else {
    console.warn(">>> [RECOVERY] allLibraryItems is MISSING!");
}

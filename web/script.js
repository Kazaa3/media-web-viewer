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

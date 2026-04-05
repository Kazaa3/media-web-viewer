# Logbuch-Eintrag

Datum: 25.03.2026

## Layout-Stabilisierung & Selenium-Test-Suite-Upgrade

### Zusammenfassung
- Layout-Probleme ("Phantom Sidebar", Zentrierung) in Logbuch- und Video-Tabs behoben.
- Selenium-Test-Suite um "PP Mode" (Performance Mode) und Session-Sync erweitert.

### Details

#### Layout-System-Stabilisierung
- Sidebar und Splitter werden in allen Nicht-Audio-Tabs per `display: none !important` entfernt, Flex-Berechnung ist korrekt.
- `#main-content-area` erhält in Management-Mode `width: 100%` und `margin-left: 0` für echtes Fullscreen.
- `tabMap`-IDs für Reporting, Video und Playlist korrigiert, keine leeren/broken Views mehr.

#### Selenium Suite Upgrade: "PP Mode" & Session Sync
- Neuer UI- und Backend-Flag für "PP Mode" (Performance Mode): Schnellere, robustere Navigation und DOM-Prüfung.
- Session-Attach: Nutzung von 127.0.0.1:9222 für aktive Browser-Session.
- Navigation-Selectoren aktualisiert: Korrekte DOM-IDs für alle Tab-Trigger-Buttons.
- DOM-Balance-Auditing: Test-Suite prüft jetzt auch komplexe Panels wie Logbuch und Video auf strukturelle Integrität.

### Geänderte Dateien
- `app.html`: `switchTab`-Logik, CSS-Layout, Selenium-UI-Flags
- `main.py`: Eel-Exposures für Selenium-Flags
- `test_selenium_session.py`: Button-Mappings, Performance Mode




*Automatisch generierter Logbucheintrag zur heutigen Layout-Stabilisierung und Test-Suite-Verbesserung.*

Ich habe die gewünschten Layout-Änderungen implementiert, um die Benutzeroberfläche je nach Ansicht zu optimieren:

**Hauptänderungen:**

- **Dynamische Sidebar-Sichtbarkeit:**
	- Die Main Sidebar (Artwork & Metadaten des aktuellen Songs) wird in den Bereichen Bibliothek, Item, Datei, Edit und Optionen ausgeblendet, sodass diese Tabs die volle Bildschirmbreite nutzen können.
	- Die Sidebar bleibt exklusiv dem Player-Tab vorbehalten, wo sie als Ergänzung zur Playlist-Verwaltung dient.

- **Optionale Minimal-Player-Ansicht:**
	- Über eine neue Einstellung im Optionen-Menü ("Minimal-Player Ansicht") können die Navigationstabs (Bibliothek bis Optionen) im Player-Modus vollständig ausgeblendet werden.
	- Gleichzeitig wird die schmale Statusleiste am unteren Rand (die "Leiste im Audioplayer") ausgeblendet, damit der Player bündig mit der Taskleiste abschließt.

- **Persistenz:**
	- Diese Einstellungen werden dauerhaft in der config.json gespeichert.
	- Schaltet man die "Minimal-Player Ansicht" in den Optionen aus, kehrt das System zum Standard-Layout zurück (Sidebar in allen Tabs sichtbar).

**Ergebnisse:**

- Bibliothek, Item, Datei, Edit, Optionen: Volle Breite, keine Sidebar (fokussiertes Arbeiten/Suchen).
- Player: Fokus auf Musik, Sidebar mit Artwork sichtbar (oder minimalistisch ohne Tabs/Statusleiste).
- Management-Tabs (Debug, Tests, Reporting, etc.): Bleiben wie gewohnt im Full-Width-Modus ohne Sidebar.

Die Funktionalität wurde in die zentrale `switchTab`-Logik der `app.html` integriert, um einen flüssigen Wechsel zwischen den Modi zu gewährleisten.

---

**Technischer Auszug (switchTab-Logik, Sidebar/Management-Layout):**

```js
const targetId = tabMap[tabId];
if (targetId) {
	const sidebar = document.getElementById('main-sidebar');
	const splitter = document.getElementById('main-splitter');
	const contentArea = document.getElementById('main-content-area');
	// Define tabs that should use the full-width layout (no main sidebar)
	// Now including standard navigation tabs (library, item, file, edit, options) as requested by the user
	const managementTabs = ['library', 'item', 'file', 'edit', 'options', 'debug', 'tests', 'reporting', 'logbuch', 'playlist', 'vlc', 'video', 'tools', 'parser'];
	const isManagement = managementTabs.includes(tabId);
	const isSidebarVisible = !isManagement;
	// Force Layout Mode
	document.body.setAttribute('data-layout-mode', isManagement ? 'management' : 'standard');
	// Hard-toggle Global UI Components
	if (sidebar) {
		if (isManagement) {
			sidebar.style.display = 'none';
			sidebar.classList.add('hidden-collapse');
		} else {
			sidebar.style.display = 'flex';
			sidebar.style.width = '300px';
			sidebar.classList.remove('hidden-collapse');
		}
	}
	// ... (weitere Layout- und Splitter-Logik)
}
```

Diese Logik sorgt dafür, dass die Sidebar und das Layout je nach Tab dynamisch angepasst werden. Die Management-Tabs nutzen die volle Breite, während der Player-Tab die Sidebar exklusiv anzeigt.

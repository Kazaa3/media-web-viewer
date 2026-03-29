# Logbuch-Eintrag

Datum: 25.03.2026

## Layout- und Scroll-Fixes für Management-Tabs

### Zusammenfassung
- Finalisierung der Layout-Anpassungen für Debug, Parser und Logbuch Tabs.
- Einheitliches 50/50 Split-Layout für alle Management-Tabs.
- Scroll-Probleme im Logbuch-Tab behoben.

### Details
1. **Zentrierte Split-Layouts (50/50)**
   - Debug Tab: Sidebar und Konsole nutzen jetzt beide `flex: 1` für eine mittige Trennung.
   - Parser Tab: Linke Settings-Pane von fixer Breite (400px) auf `flex: 1` geändert.
   - Logbuch Tab: Eintragsliste (Sidebar) von 360px auf `flex: 1` geändert, für symmetrische Aufteilung.

2. **Scroll-Fix im Logbuch**
   - `min-height: 0` für alle relevanten Flex-Container gesetzt, damit `overflow-y: auto` korrekt funktioniert.
   - Scrollbars explizit aktiviert und die Klasse `scrolling-view` für Eintragsliste und Viewer gesetzt.
   - `scroll-behavior: smooth` und einheitliches Padding für bessere UX.

### Ergebnis
- Alle Management-Tabs sind jetzt optisch und funktional konsistent.
- Logbuch-Tab ist bei langen Einträgen vollständig scrollbar und benutzbar.

---

*Automatisch generierter Logbucheintrag zu den heutigen UI-Verbesserungen.*

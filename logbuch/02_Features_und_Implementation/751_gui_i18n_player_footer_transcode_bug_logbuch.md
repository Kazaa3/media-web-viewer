---

# Logbuch-Eintrag: i18n-Tags im Player-Footer und Transcode-Modus funktionieren nicht (März 2026)

## Problemstellung

Drei zentrale i18n-Tags im Player-Footer und bei der Transcode-Anzeige funktionieren nicht wie erwartet:

1. **player_status_playing** (z.B. „Spielt:“)
2. **player_status_by** (z.B. „von“)
3. **player_ffmpeg_transcode** (z.B. „FFmpeg (Transcode)“ in der Modus-Auswahl)

---

## Symptome
- Die Übersetzungen erscheinen nicht, obwohl data-i18n-Attribute gesetzt sind.
- Es werden Fallback-Texte oder gar keine Texte angezeigt.

---

## Ursachen (Vermutung)
- i18n-Initialisierung wird nach DOM-Änderung (z.B. Tab-Wechsel, dynamisches Einblenden) nicht erneut ausgeführt.
- Die Keys fehlen oder sind falsch geschrieben in i18n.json.
- Bei dynamisch erzeugten Elementen fehlt das data-i18n-Attribut oder es wird nicht korrekt gesetzt.
- Der Transcode-Status-Text (z.B. "on-the-fly transcodiert") wird dynamisch per JavaScript gesetzt und nicht über die i18n-Logik (t('...') oder data-i18n), daher erscheint keine Übersetzung.

---

## Maßnahmen & Empfehlungen
- Prüfen, ob die Keys exakt so in i18n.json existieren.
- Sicherstellen, dass nach jedem DOM-Update die i18n-Initialisierung erneut aufgerufen wird.
- Kontrollieren, ob die data-i18n-Attribute auch bei dynamisch erzeugten Elementen gesetzt sind.
- Dynamisch gesetzte Status-Texte (wie der Transcode-Status) immer über die i18n-Logik setzen, z.B. t('player_transcode_onthefly') statt festem String.
- Prüfen, ob der Key (z.B. player_transcode_onthefly) in i18n.json existiert und korrekt übersetzt ist.

---

## Fazit

Die technische Verbindung zur i18n-Logik ist vorhanden, aber die Übersetzungen erscheinen nicht zuverlässig. Ursache sind meist fehlende oder falsch getriggerte i18n-Updates oder fehlerhafte Keys. Eine gezielte Prüfung und Nachbesserung ist erforderlich, um die Internationalisierung im Player-Footer und bei der Transcode-Anzeige sicherzustellen.

---

---

# Logbuch-Eintrag: Transcode-Status nicht i18n-fähig – Player-Footer korrekt angebunden (März 2026)

## Analyse

- Die Status-Texte im Player-Footer („Spielt:“, „von“) werden korrekt mit t('player_status_playing') und t('player_status_by') aus i18n.json gesetzt. Die Übersetzungen sind für beide Sprachen vorhanden und werden angezeigt.
- Der Transcode-Status („on-the-fly transcodiert“) ist aktuell nicht internationalisiert. Es gibt keinen eigenen i18n-Key und der Text wird als fester String im JavaScript gesetzt.

---

## Empfehlung

- Für den Transcode-Status sollte ein eigener i18n-Key (z.B. player_transcode_onthefly) in i18n.json ergänzt werden.
- Im JavaScript muss der Status-Text über t('player_transcode_onthefly') gesetzt werden, nicht als fester String.
- Nach Ergänzung des Keys und Anpassung des Codes wird die Übersetzung für den Transcode-Status wie bei den anderen Player-Texten funktionieren.

---

## Fazit

Die Player-Footer-Labels sind i18n-fähig und korrekt angebunden. Der Transcode-Status muss noch über die i18n-Logik angebunden werden, um eine vollständige Internationalisierung zu gewährleisten.

---

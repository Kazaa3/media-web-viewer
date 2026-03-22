<!-- Category: Documentation -->
<!-- Title_DE: Internationalisierung & i18n -->
<!-- Title_EN: Internationalization & i18n -->
<!-- Summary_DE: Implementierung der Mehrsprachigkeit: Übersetzungssystem, i18n.json Architektur und zweisprachige Dokumentations-Strategie. -->
<!-- Summary_EN: Implementing multi-language support: translation system, i18n.json architecture and bilingual documentation strategy. -->
<!-- Status: ACTIVE -->

# Internationalisierung & i18n

## Brückenschlag zwischen Sprachen
Ein modernes Tool wie **dict** muss global verständlich sein. Daher wurde von Anfang an auf eine konsequente Internationalisierung (i18n) gesetzt, die sowohl die Benutzeroberfläche als auch die technische Dokumentation umfasst.

## Das i18n-System
Die gesamte Logik für Übersetzungen ist in der Datei `web/i18n.json` zentralisiert.

### Technische Umsetzung
- **Translation-Keys:** Jedes UI-Element im Frontend besitzt ein `data-i18n` Attribut, das auf einen Key in der JSON-Datei verweist (z. B. `nav_library`, `btn_scan`).
- **Dynamic Loading:** Beim Sprachwechsel (🇩🇪/🇬🇧) wird das DOM in Echtzeit aktualisiert, ohne die Seite neu laden zu müssen.
- **Fallback-Mechanismus:** Sollte ein Key in einer Sprache fehlen, greift das System automatisch auf das Default-Dictionary (meist Deutsch) zurück.

## Zweisprachige Dokumentation
Ein Alleinstellungsmerkmal von dict ist die zweisprachige Führung des Logbuchs:
- **Header:** Alle Log-Einträge besitzen DE und EN Header für schnelle Auffindbarkeit.
- **Inhalt:** Während die Detailtexte nun primär in Deutsch verfasst werden (um die Geschichte von dict präzise zu erzählen), bleiben die Navigationsstrukturen und Zusammenfassungen bilingual.

## Stabilisierung & Tests
Um sicherzustellen, dass keine "toten" Keys oder unübersetzten Stellen existieren, wurde eine eigene Test-Suite implementiert:
- **`test_i18n_completeness.py`:** Prüft, ob alle genutzten Keys in der JSON-Datei vorhanden sind.
- **Deep Scans:** Erkennt hardcodierte Strings im JavaScript-Code, die noch in das i18n-System überführt werden müssen.

*Durch dieses System bleibt dict flexibel für neue Sprachen und garantiert eine konsistente User-Experience über alle Sprachgrenzen hinweg.*

<!-- lang-split -->

# Internationalization & i18n

## Bridging the languages
A modern tool like **dict** must be understood globally. Therefore, a consistent internationalization (i18n) was implemented from the start, encompassing both the user interface and the technical documentation.

## The i18n system
The entire logic for translations is centralized in the file `web/i18n.json`.

### Technical Implementation
- **Translation Keys:** Every UI element in the frontend has a `data-i18n` attribute that refers to a key in the JSON file (e.g., `nav_library`, `btn_scan`).
- **Dynamic Loading:** When the language is changed (🇩🇪/🇬🇧), the DOM is updated in real time without having to reload the page.
- **Fallback Mechanism:** If a key is missing in one language, the system automatically falls back to the default dictionary (mostly German).

## Bilingual Documentation
A unique feature of dict is the bilingual management of the logbook:
- **Header:** All log entries have DE and EN headers for quick findability.
- **Content:** While the detailed texts are now primarily written in German (to tell the story of dict precisely), the navigation structures and summaries remain bilingual.

## Stabilization & Tests
To ensure that no "dead" keys or untranslated spots exist, a separate test suite was implemented:
- **`test_i18n_completeness.py`:** Checks whether all used keys are present in the JSON file.
- **Deep Scans:** Detects hardcoded strings in the JavaScript code that still need to be transferred to the i18n system.

*Through this system, dict remains flexible for new languages and guarantees a consistent user experience across all language borders.*

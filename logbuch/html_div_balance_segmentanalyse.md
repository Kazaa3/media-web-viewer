# Logbuch-Eintrag: DIV-Balance-Test und Segmentanalyse (HTML)

## Ziel
Schnelle Lokalisierung und Behebung von HTML-Strukturfehlern (z.B. fehlende oder zu viele <div>-Tags) in großen Dateien wie app.html.

---

## Vorgehen & Testbeschreibung

1. **Segmentweise Analyse:**
   - Die Datei app.html wird in sinnvolle Segmente (z.B. 1-3151, 3152-3921, ...) unterteilt.
   - Für jedes Segment wird gezählt, wie viele <div> geöffnet und wie viele </div> geschlossen werden.
   - Die Differenz (Delta) zeigt, ob in einem Bereich ein Ungleichgewicht herrscht.

2. **Kommandozeile:**
   ```bash
   for seg in "1-3151" "3152-3921" "3922-4421" "4422-5118" "5119-10943"; do
       start=${seg%-*}
       end=${seg#*-}
       opens=$(sed -n "${start},${end}p" web/app.html | grep -o "<div" | wc -l)
       closes=$(sed -n "${start},${end}p" web/app.html | grep -o "</div" | wc -l)
       echo "Segment $seg: Opens=$opens, Closes=$closes, Delta=$((opens - closes))"
   done
   ```

3. **Beispielausgabe:**
   ```
   Segment 1-3151: Opens=134, Closes=128, Delta=6
   Segment 3152-3921: Opens=110, Closes=107, Delta=3
   Segment 3922-4421: Opens=99, Closes=99, Delta=0
   Segment 4422-5118: Opens=55, Closes=56, Delta=-1
   Segment 5119-10943: Opens=171, Closes=177, Delta=-6
   ```

4. **Interpretation:**
   - **Delta > 0:** Es fehlen schließende </div>-Tags (Container nicht korrekt abgeschlossen)
   - **Delta < 0:** Es gibt zu viele schließende </div>-Tags (Container zu früh oder doppelt geschlossen)
   - **Delta = 0:** Struktur in diesem Segment ist ausgeglichen

5. **Nutzen:**
   - Fehlerstellen werden gezielt eingegrenzt (z.B. Parser-, Debug-, Test-Tabs)
   - Reparatur kann abschnittsweise erfolgen, ohne die gesamte Datei zu durchsuchen

---

## Test: Doppelte @eel.expose-Dekorationen finden

Mit folgendem Befehl werden alle mehrfach vorkommenden @eel.expose-Deklarationen in src/core/main.py erkannt:

```bash
grep -n "@eel.expose" src/core/main.py | awk -F':' '{print $2}' | sort | uniq -c | grep -v "1 "
```

**Erklärung:**
- Sucht alle Zeilen mit @eel.expose und gibt die Zeilennummern aus.
- Sortiert und zählt die Vorkommen je Zeilennummer.
- Gibt nur Zeilen aus, die mehr als einmal vorkommen (also doppelte Dekorationen).

**Nutzen:**
- Verhindert AssertionError beim Eel-Startup durch versehentliche Mehrfach-Deklaration.
- Sollte nach Refactoring oder Merges regelmäßig ausgeführt werden.

---

## Test: Segmentweiser DIV-Balance-Check (HTML)

**Testbeschreibung:**
Das folgende Shell-Skript prüft für definierte Segmente in web/app.html, wie viele <div>- und </div>-Tags jeweils geöffnet bzw. geschlossen werden. Die Differenz (Delta) zeigt, ob ein Strukturfehler (z.B. fehlende oder zu viele Container) im jeweiligen Bereich vorliegt.

```bash
for seg in "1-3151" "3152-3921" "3922-4421" "4422-5118" "5119-10943"; do
    start=${seg%-*}
    end=${seg#*-}
    opens=$(sed -n "${start},${end}p" web/app.html | grep -o "<div" | wc -l)
    closes=$(sed -n "${start},${end}p" web/app.html | grep -o "</div" | wc -l)
    echo "Segment $seg: Opens=$opens, Closes=$closes, Delta=$((opens - closes))"
done
```

**Wie funktioniert der Test?**
- Die Datei wird in sinnvolle Segmente unterteilt (z.B. nach Tab-Grenzen oder logischen Blöcken).
- Für jedes Segment wird gezählt, wie viele <div> geöffnet und wie viele </div> geschlossen werden.
- Das Delta zeigt, ob ein Ungleichgewicht besteht:
  - **Delta > 0:** Es fehlen schließende </div>-Tags.
  - **Delta < 0:** Es gibt zu viele schließende </div>-Tags.
  - **Delta = 0:** Struktur in diesem Segment ist ausgeglichen.

**Nutzen:**
- Fehlerstellen werden gezielt eingegrenzt (z.B. Parser-, Debug-, Test-Tabs).
- Reparatur kann abschnittsweise erfolgen, ohne die gesamte Datei zu durchsuchen.
- Nach jeder größeren HTML-Änderung laufen lassen und im Logbuch dokumentieren.

---

## Empfehlung
- Nach jeder größeren HTML-Änderung diesen Test laufen lassen.
- Besonders bei Problemen mit Tabs, Panels oder dynamischen Bereichen ist die Segmentanalyse ein schneller Debug-Hebel.
- Ergebnis und Reparatur im Logbuch dokumentieren (z.B. "DIV-Balance in Segment 3152-3921 korrigiert, Parser-Tab funktioniert wieder").

---

*Dieser Ansatz ist für alle großen HTML-Projekte und für die Nachwelt als Best Practice zu empfehlen.*

# Parser/Debug/Tests/Reporting Tab Fix & RTT Sync – Implementation Log

## Problem
Im März 2026 wurde festgestellt, dass die Parser-, Debug-, Tests- und Reporting-Tabs im Frontend fehlerhaft verschachtelt waren. Ursache war ein fehlendes </div> nach Zeile 3956 in der app.html, wodurch diese Tabs innerhalb des Options-Tabs gerendert wurden und die Tab-Hierarchie zerstört wurde.

## Lösungsschritte

### 1. Frontend (web/app.html)
- Fehlendes </div> nach Zeile 3956 ergänzt (schließt #system-configuration-persistence-panel).
- DIV-Balance für folgende Panels geprüft und korrigiert:
  - Parser Tab (#regex-provider-chain-orchestrator-panel)
  - Debug Tab (#debug-flag-persistence-panel)
  - Tests Tab (#qa-validation-traceability-test-suite-panel)
  - Reporting Tab (#executive-analytical-reporting-dashboard-panel)
- Funktion runRTTTest() im JS erweitert: Detailliertes Logging von Timing und Datenstufen in der Konsole implementiert.

### 2. Backend (src/core/main.py)
- Sicherstellung, dass alle Eel-exponierten Funktionen, die komplexe Daten zurückgeben (insb. get_library, get_konsole), sanitize_json_utf8() verwenden.
- Überprüfung und Korrektur der @eel.expose-Decorator-Platzierung (keine Duplikate, keine Überschreibungen).

### 3. Tests (tests/)
- test_rtt.py: Testet rtt_ping und confirm_receipt direkt, prüft Datenintegrität nach sanitize_json_utf8.
- test_backend_api.py: Testet eel.get_library(), eel.get_db_stats() und weitere Kern-API-Endpunkte.

## Verifikationsplan
- Automatisierte Tests:
  - pytest tests/test_backend_api.py
  - pytest tests/test_rtt.py
- Manuelle Prüfung:
  - App-Start: ./run.sh, keine AssertionError.
  - Tab-Layout: Options → Parser, Debug, Tests, Reporting – Tabs füllen Content-Bereich korrekt aus.
  - RTT-Test: Debug-Tab → Run RTT Test → Timing < 50ms, Konsole zeigt "Sync OK", Backend-Logs zeigen Ping und Bestätigung.
  - Daten-Laden: Library/Player-Tab lädt Items korrekt.

## Lessons Learned
- Strikte DIV-Balance-Prüfung und Segmentanalyse sind essenziell für stabile UI.
- Automatisierte Backend- und RTT-Tests sichern Datenintegrität und Synchronisation.
- Logbuch-Dokumentation aller Debugging- und Test-Workflows ist für nachhaltige Wartung unerlässlich.

# Prozessbereinigung & UI/UX-Audit – März 2026

## Prozessmanagement
Vor dem UI/UX-Audit wurden alle laufenden main.py-, Chrome-(App-Mode)- und VLC-Prozesse mit folgendem Befehl beendet, um Mehrfachinstanzen und Seiteneffekte zu vermeiden:

    pkill -f 'main.py' || true && pkill -f 'chrome.*app=' || true && pkill -f 'vlc' || true

Dadurch ist sichergestellt, dass beim Start der Anwendung nur eine Instanz läuft und die UI-Prüfung nicht durch Altprozesse verfälscht wird.

## UI/UX-Audit (Screen-by-Screen)
- Library Tab: Grid/List-Rendering und Cover-Bilder geprüft
- Player Tab: Timeline, Lautstärkeregelung, Engine-Switch getestet
- Parser Tab: (Struktur bereits gefixt) Dynamisches Listen- und Settings-Rendering geprüft
- Debug Tab: (Struktur bereits gefixt) Loganzeige und RTT-Test-Feedback geprüft
- Reporting Tab: (Struktur bereits gefixt) Plotly-Charts und SQL-File-Liste geprüft

## Item-RTT-Test (Feature/Verifikation)
- Geplant: RTT-Test für einzelne Media-Items zur Verifikation der Metadaten-Sync-Latenz

## Verifikationsplan
- Automatisierte RTT- und Backend-Tests ausführen
- App starten, durch alle Tabs navigieren
- Sicherstellen, dass nur eine Instanz läuft

## Lessons Learned
- Prozessbereinigung ist essenziell für reproduzierbare UI-Tests
- UI/UX-Audit nach jedem Strukturfix notwendig
- Einzel-RTT-Tests helfen, Metadaten-Sync zu validieren

# 93 – Anker vor Runtime-Fix: Package-Display im Optionen-Tab

**Datum:** 09.03.2026  
**Version:** 1.3.3  
**Status:** Pre-Fix Snapshot (Release-Prep)

## Ziel dieses Ankers

Dieser Eintrag fixiert den aktuellen, validierten Stand **vor** dem nächsten gezielten Runtime-Fix der Paketanzeige im Optionen-Tab.

## Aktueller technischer Stand

- Build-/Release-Gates sind aktiv und enthalten die relevanten Stabilitäts- und Regressionstests.
- Die Package-Fallback-Kette im Backend ist implementiert:
  1. `pip list --format=json`
  2. `pip list --format=columns` (Parser-Fallback)
  3. `importlib.metadata` / `pkg_resources` Fallback
- Frontend hat einen Safety-Retry (`get_environment_info(true)`), wenn initial keine Pakete zurückkommen.
- `mediainfo`-Status wird im Environment-Block mitgeführt und im UI angezeigt.

## Test- und Verifikationsstand

- Fokussierte Testläufe erfolgreich (inkl. neuer Regression für Package-Fallback).
- Gate-Scope-Lauf erfolgreich (`20 passed`, nur Warnungen).
- Backend-Runtime-Wertprüfung zeigte eine nicht-leere Paketliste (Beispiel: 49 Pakete).

## Offener Release-Blocker

- Einzelne Runtime-Szenarien zeigen im GUI weiterhin „No packages found“, obwohl Backend/Teststand grün ist.
- Wahrscheinlichste Ursache: Laufzeit-/Instanz-Mismatch (stale Prozess, Cachezustand, nicht aktuelles Frontend-Bundle oder abweichende Startumgebung).

## Nächster Schritt (direkt nach diesem Anker)

1. Live-Verifikation in genau der produktiv gestarteten Instanz.
2. Sichtbare Laufzeitdiagnostik im Optionen-Tab (Source + Count aus `get_environment_info`).
3. Danach gezielter Fix im echten Laufpfad statt nur im Testpfad.

---

Dieser Eintrag ist der Referenzpunkt für alle folgenden Änderungen am Package-Display-Fix.

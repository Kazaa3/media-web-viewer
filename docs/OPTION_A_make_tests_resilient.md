**Option A — Tests resilient machen (Empfohlen)**

Kurz: Mach die Test-Suite robust gegenüber lokalen Entwicklungsumgebungen, indem wir
gezielt Collection-/Runtime-Gates, leichte Kompatibilitäts-Shims und automatisches
Skipping für externe Abhängigkeiten (ffprobe, mkvmerge, Testdaten) hinzufügen.

Vorteile:
- Schnellere, zuverlässigere lokale Runs für Entwickler.
- Geringe bis keine Änderungen an CI oder externen Abhängigkeiten.
- Fokus auf Unit-Level-Qualität; Integrationstests bleiben optional/markiert.

Nachteile:
- Tests greifen weniger streng auf Integrationsebene — einige Fehlermodi werden erst
  im CI oder mit vollständiger Umgebung sichtbar.
- Erfordert Pflege von Skip-Regeln und Kompatibilitäts-Shims.

Konkrete Schritte:
1. Collection-Time Guards
   - Erweitere `conftest.py` mit heuristischen Prüfungen (binaries, testdata, network)
     und setze `pytest.mark.skip` mit klaren Gründen.
2. Kompatibilitäts-Shims
   - Leichte factory-/shim-Objekte für fragile Drittanbieter-APIs (z.B. `MP4Chapters`).
   - Normalize-Routinen für parser-Return-Formate (tuple/dict) in `models.py`.
3. Test-Scoped Guards
   - In tests, um Dateizugriffe (`media/test_cover.jpg`, `testdata/*`) `try/except`
     oder `pytest.skip` bei fehlenden Assets.
4. Fallback-Implementationen
   - Für parser/ffprobe-Funktionen: returniere leere/harmless dicts statt None,
     damit `MediaItem`-Konstruktoren nicht abstürzen.
5. Dokumentation
   - Ergänze `README.md` oder `docs/` um „Running tests locally“ mit empfohlenen
     quick-setup-Schritten.

Beispiel-Befehle (lokal):
```bash
# virtuelles Environment aktivieren
source .venv/bin/activate

# vollständige Tests (mit größeren Integrations-Tests überspringen automatisch)
pytest -q

# einzelner Test zur Verifikation
pytest tests/test_media_type_consistency.py -q
```

Wann wählen:
- Wenn das Ziel ist, Entwickler-Feedback-Schleifen zu beschleunigen und das Repo
  für Contributor stabiler zu machen. Empfohlen für aktive Feature-Entwicklung.

**Option B — Testdaten hinzufügen & Abhängigkeiten pinnen**

Kurz: Sorge für deterministische Integrationstests durch Bereitstellung der
fehlenden `testdata/`-Assets und durch Festschreiben (pinning) von Drittanbieter-
Bibliotheken (z.B. `mutagen`, `pymediainfo`, `ffmpeg/ffprobe`) in `requirements.txt` oder
`requirements-test.txt`.

Vorteile:
- Integrationstests laufen deterministisch und reproduzierbar.
- Besseres Coverage für echte Laufzeitprobleme (FFmpeg/ffprobe-Interaktionen).

Nachteile:
- Größerer initialer Aufwand (Sammeln/lichtrechtliche Bereitstellung der Testdaten).
- Risiko, dass die pinned Versionsauswahl später aktualisiert/gewartet werden muss.

Konkrete Schritte:
1. Testdaten-Sammlung
   - Sammle die benötigten Dateien (`mkv`, `mp4`, `cover.jpg`, sample audio) in
     `tests/testdata/` und schreibe ein kurzes `tests/testdata/README.md` mit Quellen.
   - Prüfe Lizenzen; wenn notwendig, erstelle kleine synthetische Fixtures (ffmpeg erzeugt
     test-clips) statt urheberrechtlich geschützter Inhalte.
2. Pin Dependencies
   - Erstelle `requirements-test.txt` mit festen Versionen, z.B.:
     - mutagen==x.y.z
     - pymediainfo==a.b.c
   - Ergänze `pyproject.toml` oder `requirements.txt` entsprechend (Dokumentation).
3. CI / Local Setup
   - CI-Runner aktualisieren, damit `pip install -r requirements-test.txt` vor Tests läuft.
   - Optional: provide a Dockerfile/test image that pre-installs native binaries
     (ffmpeg/ffprobe, mkvmerge) for CI reproducibility.
4. Test-Verifizierung
   - Run the full suite in a clean environment (Docker or fresh venv) and iterate
     on pins until the suite is stable.

Beispiel-Befehle (lokal/CI):
```bash
# create test venv and install pinned test deps
python -m venv .venv-test
source .venv-test/bin/activate
pip install -r requirements-test.txt

# run full tests
pytest -q
```

Wann wählen:
- Wenn die priority ist, Integrationstests deterministisch in CI zu fahren und
  reale parser-/binary-Interaktionen abzusichern (trade-off: maintenance effort).

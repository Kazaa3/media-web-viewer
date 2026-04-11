<!-- Status: DRAFT -->
date: 2026-03-11
category: docs
tags: [cli, mwv-cli, docker, headless]

# `mwv-cli` — Command Line Interface für MediaWebViewer

Kurz: Dokumentation der minimalen CLI für headless / CI‑oriented usage. Ziel: einfache, reproduzierbare Ausführung von Parsing/Health/Logs/ffprobe‑tasks ohne GUI.

## Übersicht
`mwv-cli` ist ein kleiner Entrypoint für server‑seitige Tasks. Er läuft in drei Modi:
- `parse <path>` — Extrahiere Metadaten für Datei/Verzeichnis (delegiert an `extract_metadata`).
- `health` — Gibt `get_server_status()` als JSON aus.
- `logs [--limit N]` — Liefert die letzten N Log‑Einträge (default 200).
- `ffprobe <file> [--json] [--output <file>]` — Nutzt sicheren ffprobe‑Wrapper; fällt auf `pymediainfo` zurück wenn nötig.

## Exit‑Codes
- `0` — Erfolg
- `1` — Fehler (z. B. ungültige Argumente)
- `2` — Laufzeitfehler beim Ausführen der Aufgabe (z. B. Parser‑Fehler)

## Beispiele
- Parse und Ausgabe in Datei:

```bash
mwv-cli parse /media/smb/song.mp3 --output /tmp/song.meta.json
```

- Health check (JSON auf stdout):

```bash
mwv-cli health
```

- Letzte 100 Logs anzeigen:

```bash
mwv-cli logs --limit 100
```

- ffprobe (JSON) mit Fallback:

```bash
mwv-cli ffprobe /media/smb/clip.mp4 --json --output /tmp/clip.ffprobe.json
```

## Docker / Headless Integration
- Empfohlenes Deployment: Host mountet SMB/CIFS laufwerk in Container read‑only.
- Docker‑Modi:
  - `MODE=server` — Standardserver (Eel optional)
  - `MODE=headless` — backend only; Eel/GUI deaktiviert
  - `MODE=cli` — startet `mwv-cli` mit den übergebenen args und beendet sich

Beispiel: Parse innerhalb eines Headless‑Containers (Host mountet /mnt/my-smb):

```bash
docker run --rm \
  -v /mnt/my-smb:/media/smb:ro \
  -e MODE=cli \
  mediawebviewer:headless \
  mwv-cli parse /media/smb/song.mp3 --output /tmp/song.meta.json
```

## Sicherheitsrichtlinien
- Keine Verwendung von `shell=True` — subprocesses werden immer mit Argument‑Listen ausgeführt.
- Validierung von Eingabe‑Pfaden (keine ungeprüften mount‑Aufrufe aus untrusted input innerhalb des Containers).
- Empfohlen: Host‑Side SMB mount mit `:ro` und Container als non‑root Nutzer ausführen.

## Implementationshinweise
Dateien/Orte zum Ergänzen:
- CLI Entrypoint: `cli.py` oder Aufruf über `main.py` (einfacher wrapper, der `argparse` nutzt).
- Safe subprocess wrapper: `tools/ffprobe_wrapper.py` (funktion `run_ffprobe(path, timeout=None)`).
- Dockerfile / docker-compose: `Dockerfile.headless`, `docker-compose.ci.yml`.

Anchor‑IDs für Arbeitsplanung:
- <!-- ANCHOR: docker-cli -->
- <!-- ANCHOR: docker-headless -->
- <!-- ANCHOR: docker-tests -->
- <!-- ANCHOR: ffprobe-fallback -->

## CI‑Hinweise
- Integration job (`backend-integration`) sollte `ENABLE_INTEGRATION=1` setzen und die Headless‑Image verwenden.
- Artefakte: `logs/`, `ffprobe/*.json`, `psutil_snapshot.json`, Parser‑output JSON.
- Tests:
  - Unit: `tests/test_cli_parse.py` (exists), `tests/test_subprocess_wrapper.py` (exists)
  - Gated Integration: `tests/test_docker_headless_integration.py` (exists, gated via `ENABLE_INTEGRATION`)

---

Erstellt als Basisdokumentation; danach PR mit `cli.py` + `Dockerfile` + CI‑Job stub empfohlen.

## Detail: `mwv-cli` Spezifikation & Beispielimplementation

Ziel: ein kleines, gut testbares CLI‑Entrypoint Modul `cli.py` mit subcommands.

Commands (kurz):
- `parse <path> [--output FILE] [--timeout N]` — ruft `extract_metadata(path, ...)` auf und schreibt JSON.
- `health` — ruft `get_environment_info()` / `get_server_status()` auf, gibt JSON zurück.
- `logs [--limit N] [--json]` — ruft `logger.get_ui_logs()` und gibt Text/JSON aus.
- `ffprobe <file> [--output FILE] [--json]` — ruft `tools.ffprobe_wrapper.run_ffprobe()` mit sicheren args.

Minimalbeispiel `cli.py` (Skizze):

```python
import argparse
import json
from main import extract_metadata, get_environment_info
from logger import get_ui_logs
from tools import ffprobe_wrapper

def main(argv=None):
    parser = argparse.ArgumentParser(prog='mwv-cli')
    sub = parser.add_subparsers(dest='cmd')

    p = sub.add_parser('parse')
    p.add_argument('path')
    p.add_argument('--output')

    sub.add_parser('health')

    l = sub.add_parser('logs')
    l.add_argument('--limit', type=int, default=200)

    f = sub.add_parser('ffprobe')
    f.add_argument('file')
    f.add_argument('--output')

    args = parser.parse_args(argv)

    if args.cmd == 'parse':
        meta = extract_metadata(args.path)
        out = json.dumps(meta, ensure_ascii=False, indent=2)
        if args.output:
            open(args.output, 'w', encoding='utf-8').write(out)
        else:
            print(out)
        return 0

    if args.cmd == 'health':
        print(json.dumps(get_environment_info(), indent=2, ensure_ascii=False))
        return 0

    if args.cmd == 'logs':
        logs = get_ui_logs()[: args.limit]
        print('\n'.join(logs))
        return 0

    if args.cmd == 'ffprobe':
        res = ffprobe_wrapper.run_ffprobe(args.file)
        out = json.dumps(res, indent=2, ensure_ascii=False)
        if args.output:
            open(args.output, 'w', encoding='utf-8').write(out)
        else:
            print(out)
        return 0

    parser.print_help()
    return 1

if __name__ == '__main__':
    raise SystemExit(main())
```

Hinweis: oben sind direkte `main`‑Aufrufe demonstrativ — in der echten Implementierung sollten die Backend‑Funktionen aus einem stabilen Modul importiert oder via ein explizites public API wrappers bereitgestellt werden, um Seiteneffekte beim Import zu vermeiden.

## Dockerfile.headless (Sketch)

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
ENV MODE=headless
ENTRYPOINT ["/usr/local/bin/python", "-m", "cli"]
```

Für CI: ein schlankeres image ohne `cifs-utils` und mit `MODE=cli` beim Ausführen.

## CI Job Stub (GitHub Actions) — backend-integration.yml (Auszug)

```yaml
name: Backend Integration
on: [push]
jobs:
  backend-integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t mwv-headless -f Dockerfile.headless .
      - name: Run parser smoke
        run: |
          docker run --rm -v ${{ github.workspace }}/tests/fixtures:/fixtures:ro -e ENABLE_INTEGRATION=1 mwv-headless mwv-cli parse /fixtures/sample.mp3 --output /fixtures/out.json
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: integration-artifacts
          path: tests/fixtures/out.json
```

## Tests & Quality
- Unit tests should import `cli` via `pytest.importorskip('cli')` until the module exists (we already added placeholders).
- Integration CI should mount `tests/fixtures/` read‑only and assert outputs.

## Next Steps (konkret)
1. Implement `cli.py` using the sketch above and ensure imports are lazy to avoid heavy side effects on import.
2. Add `tools/ffprobe_wrapper.py` with `subprocess.run([...], check=True)` semantics and `pymediainfo` fallback.
3. Add `Dockerfile.headless` and a small `docker-compose.ci.yml` for local CI debugging.
4. Create GitHub Actions job file `/.github/workflows/backend-integration.yml` from stub.

---

Erweitert: vollständige CLI‑Spec, Beispielcode, Docker‑Sketch und CI‑Job‑Stub. Nächster Schritt: implementieren (CLI + ffprobe wrapper + Dockerfile).

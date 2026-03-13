<!-- Status: DRAFT -->
date: 2026-03-11
category: plan
tags: [smb, docker, headless, cli, ci]

# SMB Pfade, Docker Headless Container & CLI — Kurzplan

Kurz: Planung für sicheren Zugriff auf SMB/CIFS Shares, ein Docker‑Container mit headless Modus und eine kleine CLI‑Schnittstelle für serverseitige Befehle (parsen, health, logs). Ziel: reproduzierbare CI‑Runs ohne GUI, sichere Subprocess‑Nutzung und einfache local/dev workflows.

## Ziele
- Sicheres, konfigurierbares Mounting/zugriff auf SMB‑Pfade für Parser und Scan‑Jobs.
- Docker‑Container: headless (kein Browser UI), optional Eel deaktiviert; befehlsorientierter CLI‑Entrypoint (`mwv-cli`) für common tasks.
- CI‑freundlich: run parsed tasks in container, capture artifacts (logs, ffprobe JSON, psutil snapshot).

## High Level Design
- SMB: Support via two patterns:
  - External mount (recommended): host mount führender SMB/CIFS Volumes; Container liest Pfade nur lesend.
  - In‑container mount (optional): use `cifs-utils` and `mount.cifs` with strict env validation. Documented but discouraged for CI/production.

- Docker modes (env driven):
  - `MODE=server` — full backend (Eel enabled if browser wanted)
  - `MODE=headless` — backend only, no GUI, Eel calls disabled; exposes CLI/HTTP for automation
  - `MODE=cli` — run `mwv-cli` then exit (one-shot tasks)

- CLI (`mwv-cli`) features: #NAME VARIABLE PROGRAMM
  - `mwv-cli parse <path>` — run `extract_metadata()` for given path and emit JSON to stdout or file
  - `mwv-cli health` — print `get_server_status()` JSON
  - `mwv-cli logs --limit N` — print recent logs
  - `mwv-cli ffprobe <file> --json` — run safe ffprobe wrapper, fallback to pymediainfo

## Security & Safety
- No `shell=True` for subprocesses; args passed as lists.
- Validate SMB path inputs (deny obvious path traversal when mounting inside container).
- Recommend host‑mounted SMB shares with read‑only permissions for the container user.
- Minimal privileges: run container as non‑root when reading external mounts.

## Dockerfile / Compose sketch
- Base image: `python:3.11-slim` plus `ffmpeg`/`ffprobe` if available; include `cifs-utils` only in optional build.
- Provide two Docker build tags: `mediawebviewer:server` and `mediawebviewer:headless` (smaller set of deps).

Example (sketch):

- Environment variables:
  - `MODE=headless|server|cli`
  - `ENABLE_INTEGRATION=1` (for CI gated integration runs)
  - `SMB_MOUNT_POINT=/media/smb` (when host mounts into container)

- Sample `docker run` for CLI parse (host mounts SMB share at /media/smb):

  docker run --rm \
    -v /mnt/my-smb-share:/media/smb:ro \
    -e MODE=cli \
    mediawebviewer:headless \
    mwv-cli parse /media/smb/song.mp3 --output /tmp/metadata.json

## CI integration notes
- Add a `backend-integration` job that uses `mediawebviewer:headless` image in `MODE=cli` or `MODE=headless`.
- Artifacts to capture: `logs/`, `ffprobe/*.json`, `psutil_snapshot.json`.
- Use host‑mounted fixtures (`tests/fixtures/`) for deterministic parser tests.

## Tests & Verification
- Unit: mock SMB inputs, validate CLI argument parsing, ensure subprocess wrapper called with list args.
- Integration (gated): run container with fixture mounts and real `ffprobe` available; validate metadata outputs and captured artifacts.

## Implementation Tasks (short)
1. Add `mwv-cli` entrypoint in `main.py` or a small `cli.py` wrapper that imports backend modules. (Anchor: <!-- ANCHOR: docker-cli -->)
2. Add Dockerfile + lightweight `docker-compose.ci.yml` for headless/cli flows. (Anchor: <!-- ANCHOR: docker-headless -->)
3. Document recommended host mount workflow in `INSTALL.md` and `logbuch`. (Anchor: <!-- ANCHOR: smb-host-mount -->)
4. Add tests: `tests/test_cli_parse.py`, `tests/test_docker_headless_integration.py` (gated). (Anchor: <!-- ANCHOR: docker-tests -->)

## Next steps
- Implement `mwv-cli` skeleton and update CI job stub. Update `logbuch` with exact Dockerfile snippets once prototype built.

---

*Created by planning note — expand into PR with code + CI changes.*

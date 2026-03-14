# Tutorial: Finalisierung v1.34 & Übergang zu Meilenstein 1

Dieses Tutorial leitet dich durch die finalen administrativen Schritte, um den gereinigten Stand von v1.34 als neue Basis im main-Branch zu etablieren und die Entwicklung des Videoplayers (Meilenstein 1) vorzubereiten.

## Status-Check
- **v1.33:** Gesichert als Git-Tag (alter main).
- **v1.34:** Gereinigter, konsolidierter Stand auf dem Branch meilenstein-1-mediaplayer.
- **Repo-Status:** Alle Debug-Flags sind zentralisiert, die Historie ist gesquasht, die Datenbank ist bereit für einen frischen Start.

## Schritt 1: Pull Request auf GitHub erstellen
Da der main-Branch geschützt ist, muss der Merge über die Web-Oberfläche erfolgen.

1. Gehe zu deinem Repository auf GitHub: https://github.com/Kazaa3/media-web-viewer
2. Klicke auf den Reiter "Pull Requests".
3. Klicke auf den grünen Button "New Pull Request".
4. Wähle als base: `main` und als compare: `meilenstein-1-mediaplayer`.
5. Klicke auf "Create Pull Request".
6. Gib ihm den Titel: `release: merge v1.34 into meilenstein-1-mediaplayer and main`.
7. Bestätige den Merge ("Merge" oder "Squash and Merge").

## Schritt 2: Lokale Synchronisation
Nachdem der PR auf GitHub gemergt wurde, müssen wir deinen lokalen main aktualisieren.

```bash
git checkout main
git pull origin main
```

## Schritt 3: Der Deployment-Test
Wir verifizieren, dass die saubere Historie und die neue Konfiguration auch im Build-Prozess funktionieren.

```bash
# Führe die volle Pipeline im Core-Venv aus
./infra/build_system.py --pipeline
```

## Schritt 4: Start Meilenstein 1 (Videoplayer)
Da v1.34 nun die stabile Basis bildet, beginnen wir mit der Implementierung des Videoplayers.

Erstelle einen Feature-Branch von main:

```bash
git checkout -b feature/m1-video-player
```

**Nächste technische Ziele:**
- Integration der HTML5 Video-Engine.
- Implementierung der Player-Controls im Frontend.
- Anbindung des Backends für Video-Streaming (VLC/FFmpeg-Support).

---

## Schritt 5: Merge von v1.34 (meilenstein-1-mediaplayer) nach main und Tagging

1. **Merge durchführen:**
   - Erstelle auf GitHub einen Pull Request von `meilenstein-1-mediaplayer` nach `main`.
   - Merge den PR ("Merge" oder "Squash and Merge").

2. **Alten main als v1.33 taggen:**
   - Vor dem Merge wurde der alte main-Stand bereits als Tag `v1.33` archiviert.

3. **Nach dem Merge:**
   - Aktualisiere deinen lokalen main:
     ```bash
     git checkout main
     git pull origin main
     ```
   - Wechsle zurück zu meilenstein-1-mediaplayer, um dort weiterzuarbeiten:
     ```bash
     git checkout meilenstein-1-mediaplayer
     ```

**Hinweis:**
- Nach dem Merge ist main offiziell auf v1.34 (purified) und bereit für produktiven Einsatz.
- Die Entwicklung für weitere Features (z.B. Videoplayer) erfolgt weiterhin auf meilenstein-1-mediaplayer oder neuen Feature-Branches.

Letzte Aktualisierung: 14.03.2026

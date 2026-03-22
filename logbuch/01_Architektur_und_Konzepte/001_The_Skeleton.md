# 01 Die Skeleton-Phase: Der Ursprung

**Datum:** 13.03.2026
**Kategorie:** Architektur, Historie
**Status:** ARCHIVED

---

## Retrospektive auf das erste MVP

Dieses Dokument ist ein Rückblick auf die allererste Phase von "dict". Das Ziel war minimalistisch: Ein funktionierendes "Skelett" zu bauen, das zeigt, dass die Integration von Python und HTML5 machbar ist.

### Die Kernkomponenten des Skeletts
- **Eel-Fenster:** Ein einfaches Browser-Fenster, das via Python (`eel.init`) gesteuert wird.
- **Listing-Engine:** Ein Python-Skript, das rekursiv das `media/` Verzeichnis scannt und die Pfade als JSON ans Frontend sendet.
- **Glassmorphism Base:** Der erste Entwurf für das dunkle, transparente Design wurde bereits hier implementiert, um den "Premium-Look" zu testen.

### Lessons Learned
Die größte Erkenntnis war, dass die bidirektionale Kommunikation via `@eel.expose` extrem performant ist, solange man keine riesigen BLOBS über die Leitung schickt. Dies bildete den Grundstein für den späteren Tab-Orchestrator und die Metadaten-Pipeline.

---

**Kommentar:**
Dieses Dokument markiert den Tag, an dem das Projekt den "Proof of Concept" Status verließ.

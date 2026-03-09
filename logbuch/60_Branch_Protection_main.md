<!-- Category: INFRASTRUCTURE -->
<!-- Status: COMPLETED -->

# Branch Protection für `main` aktiviert

## Kontext
GitHub meldete für das Repository:
> Your main branch isn't protected

Ziel war, `main` gegen versehentliche destructive Aktionen abzusichern und Merge-Qualität über PR-Regeln zu erhöhen.

## Umsetzung (2026-03-09)
Die Branch Protection wurde direkt per GitHub API (`gh api`) auf `main` gesetzt.

Verwendeter Endpunkt:
- `PUT /repos/Kazaa3/media-web-viewer/branches/main/protection`

## Aktivierte Regeln
- `allow_force_pushes: false`  
  → Force-Pushes auf `main` sind blockiert.

- `allow_deletions: false`  
  → Löschen des `main`-Branches ist blockiert.

- `required_pull_request_reviews.required_approving_review_count: 1`  
  → Mindestens 1 PR-Approval vor Merge.

- `required_pull_request_reviews.dismiss_stale_reviews: true`  
  → Bei neuen Commits werden alte Approvals ungültig.

- `required_conversation_resolution: true`  
  → Offene Review-Kommentare müssen vor Merge aufgelöst sein.

- `enforce_admins: true`  
  → Regeln gelten auch für Admins.

- `required_status_checks` aktiv (strict: false, contexts: [])  
  → Status-Check-Protection ist aktiv; konkrete Check-Namen können später ergänzt werden.

## Verifikation
Die Protection wurde im Anschluss über API-Readback bestätigt:
- `force_push: False`
- `deletions: False`
- `reviews_required: True`
- `status_checks_required: True`

## Ergebnis
`main` ist jetzt zentral geschützt und für Laptop-Arbeit stabil abgesichert:
- Keine Force-Push-Überschreibungen
- Kein Branch-Delete
- PR-basierter Merge-Flow mit Reviewpflicht

## Nächster sinnvoller Schritt
Sobald CI-Checks stabil benannt sind, `required_status_checks.contexts` auf konkrete Jobs setzen (z. B. `test`, `build`).

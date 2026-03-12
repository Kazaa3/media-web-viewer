<!-- Category: Process -->
<!-- Title_DE: Git-Strategie: Milestones & Branching -->
<!-- Title_EN: Git Strategy: Milestones & Branching -->
<!-- Summary_DE: Skalierung mit Meilensteinen und Branches, Schutz des main-Branch. -->
<!-- Summary_EN: Scaling with milestones and branches, protecting the main branch. -->
<!-- Status: COMPLETED -->
<!-- Anchor: 10_Git_Strategy_Milestones -->
<!-- Redundancy: Section covers Git milestones, branch management, merge gates, scalability. -->

# 09 Git-Strategie: Milestones & Branching

Um die wachsende Komplexität beherrschbar zu machen, wurde eine professionelle **Git-Strategie** etabliert. Dies schützt die Stabilität der Anwendung, während gleichzeitig an großen neuen Features gearbeitet wird.

### Die Meilenstein-Logik
Das Projekt ist in klar definierte **Meilensteine (M1, M2...)** unterteilt. Jeder Meilenstein hat eine spezifische Mission:
- **M1 (AudioPlayer):** Die stabile Basis. Alles, was in Entry 01-08 beschrieben wurde.
- **M2 (MediaLibrary):** Der Ausbau der Datenbank und Bibliotheksfunktionen.

### Branch-Management & Schutz
Um den `main`-Branch (die "Release-Linie") sauber zu halten, gelten strikte Regeln:
1. **Feature-Isolierung:** Neue Entwicklungen finden niemals direkt in `main` statt, sondern in dedizierten Milestone-Branches (z. B. `milestone/2-medienbibliothek`).
2. **Merge-Gates:** Bevor Code in `main` landet, muss er Validierungen durchlaufen (Version-Sync, Tests, Dokumentations-Check).
3. **Stabilität:** `main` repräsentiert immer den aktuellsten stabilen Stand, der als Paket (`.deb`, `.exe`) veröffentlich werden kann.

### Skalierbarkeit
Diese Struktur erlaubt es, parallel an Fehlerbehebungen (in `main`) und an der Zukunft (in Milestone-Branches) zu arbeiten, ohne sich gegenseitig zu blockieren. Es ist das Rückgrat für eine nachhaltige Softwareentwicklung.

<!-- lang-split -->

# 09 Git Strategy: Milestones & Branching

To keep the growing complexity manageable, a professional **Git strategy** has been established. This protects the application's stability while allowing for work on major new features in parallel.

### The Milestone Logic
The project is divided into clearly defined **milestones (M1, M2...)**. Each milestone has a specific mission:
- **M1 (AudioPlayer):** The stable baseline. Everything described in entries 01-08.
- **M2 (MediaLibrary):** Expanding the database and library features.

### Branch Management & Protection
To keep the `main` branch (the "release line") clean, strict rules apply:
1. **Feature Isolation:** New developments never happen directly in `main`, but in dedicated milestone branches (e.g., `milestone/2-medienbibliothek`).
2. **Merge Gates:** Before code lands in `main`, it must pass validations (version sync, tests, documentation check).
3. **Stability:** `main` always represents the latest stable state that can be published as a package (`.deb`, `.exe`).

### Scalability
This structure allows for parallel work on bug fixes (in `main`) and on the future (in milestone branches) without blocking each other. It is the backbone for sustainable software development.

<!-- Category: Architecture -->
<!-- Title_DE: 02 Brückenschlag: Warum Eel & Python? -->
<!-- Title_EN: 02 Bridging the Worlds: Why Eel & Python? -->
<!-- Summary_DE: Die strategische Entscheidung für die Hybrid-Architektur. -->
<!-- Summary_EN: The strategic decision for the hybrid architecture. -->
<!-- Status: COMPLETED -->

# 02 Brückenschlag: Warum Eel & Python?

Nach dem ersten erfolgreichen Wireframe stellte sich die Frage: Wie bauen wir eine App, die sich wie moderne Web-Software anfühlt, aber die Power eines lokalen Systems hat?

### Die Entscheidung: Eel
Anstatt auf schwere Frameworks wie Electron oder klassische GUIs wie Tkinter zu setzen, fiel die Wahl auf **Eel**.

1. **Frontend-Freiheit:** Wir nutzen Standard-Webtechnologien (HTML5, CSS3, JS). Das ermöglicht moderne Effekte wie Blur-Filter und CSS-Grids ohne Kopfschmerzen.
2. **Backend-Direktheit:** Python bleibt der "Stärkere" im Team. Es kümmert sich um das Dateisystem und die Binaries, während JS nur für die Anzeige zuständig ist.
3. **Bidirektionalität:** Funktionen in Python werden mit `@eel.expose` markiert und sind für JavaScript sofort greifbar – und umgekehrt.

### Erkenntnis
Dieser Brückenschlag erlaubt es uns, die Komplexität im Backend (Python) zu kapseln, während der Nutzer eine reaktive, flüssige Oberfläche erlebt. Es ist die Architektur der Wahl für den *Media Web Viewer*.

<!-- lang-split -->

# 02 Bridging the Worlds: Why Eel & Python?

After the first successful wireframe, the question arose: How do we build an app that feels like modern web software but has the power of a local system?

### The Decision: Eel
Instead of relying on heavy frameworks like Electron or classic GUIs like Tkinter, the choice was **Eel**.

1. **Frontend Freedom:** We use standard web technologies (HTML5, CSS3, JS). This allows for modern effects like blur filters and CSS grids without headaches.
2. **Backend Directness:** Python remains the "stronger" member of the team. It handles the file system and binaries, while JS is only responsible for the display.
3. **Bidirectionality:** Functions in Python are marked with `@eel.expose` and are immediately accessible to JavaScript – and vice versa.

### Insight
This bridge allows us to encapsulate complexity in the backend (Python) while the user experiences a reactive, fluid interface. It is the architecture of choice for the *Media Web Viewer*.

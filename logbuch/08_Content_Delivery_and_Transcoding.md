<!-- Category: Development -->
<!-- Title_DE: Content-Delivery & Transcoding -->
<!-- Title_EN: Content Delivery & Transcoding -->
<!-- Summary_DE: Hybrid-Ansatz für Medienbereitstellung und On-the-fly Transcoding. -->
<!-- Summary_EN: Hybrid approach for media delivery and on-the-fly transcoding. -->
<!-- Status: COMPLETED -->

# Content-Delivery & Transcoding

Um Medieninhalte effizient und kompatibel im Browser abzuspielen, nutzt der *Media Web Viewer* einen hybriden Mechanismus zur Bereitstellung und Konvertierung.

### Bottle als Media-Server
Während Eel die GUI steuert, fungiert ein interner **Bottle-Webserver** als dedizierter Provider für Binärdaten. Er stellt Routen bereit wie:
- `/media/<path>`: Liefert die eigentliche Audio-/Videodatei.
- `/cover/<path>`: Liefert das extrahierte Cover-Bild.

### On-the-fly Transcoding
Eines der mächtigsten Features ist die automatische Transkodierung. Viele Browser unterstützen nativ keine Formate wie ALAC oder bestimmte WMA-Profile. 
Das Backend erkennt diese Inkompatibilität anhand der Dateiendung oder der Metadaten und startet im Hintergrund einen **FFmpeg-Stream**:
- Die Datei wird in Echtzeit in ein kompatibles Format (z.B. FLAC oder OGG) umgewandelt.
- Der konvertierte Stream wird direkt an den Player gesendet, ohne die gesamte Datei vorab konvertieren zu müssen.
- Häufig genutzte Transkodes werden im `.cache`-Verzeichnis zwischengespeichert, um die CPU-Last bei wiederholtem Abspielen zu minimieren.

Dieser Ansatz kombiniert maximale Formatunterstützung mit minimaler Wartezeit für den Nutzer.

<!-- lang-split -->

# Content Delivery & Transcoding

To play media content efficiently and compatibly in the browser, the *Media Web Viewer* uses a hybrid mechanism for delivery and conversion.

### Bottle as Media Server
While Eel controls the GUI, an internal **Bottle web server** acts as a dedicated provider for binary data. It provides routes such as:
- `/media/<path>`: Delivers the actual audio/video file.
- `/cover/<path>`: Delivers the extracted cover image.

### On-the-fly Transcoding
One of the most powerful features is automatic transcoding. Many browsers do not natively support formats like ALAC or certain WMA profiles. 
The backend detects this incompatibility based on the file extension or metadata and starts an **FFmpeg stream** in the background:
- The file is converted in real time into a compatible format (e.g., FLAC or OGG).
- The converted stream is sent directly to the player without having to convert the entire file beforehand.
- Frequently used transcodes are cached in the `.cache` directory to minimize CPU load during repeated playback.

This approach combines maximum format support with minimal waiting time for the user.

<!-- Category: Release -->

# Release v1.1.10 – Stabilität & Packaging

In diesem Meilenstein wurde die Anwendung für die öffentliche Freigabe finalisiert. Der Schwerpunkt lag auf der Systemintegration unter Linux und der Bereinigung der Benutzeroberfläche.

## Highlights

### 1. Robustes .deb Packaging
- Native Abhängigkeiten wie `python3-tk` (für Ordner-Dialoge), `libmediainfo0v5` und `ffmpeg` werden nun automatisch über das Paketmanagement aufgelöst.
- Das Paket erstellt automatisch eine virtuelle Python-Umgebung (`.venv`) in `/opt/media-web-viewer`, um Konflikte mit System-Paketen zu vermeiden.

### 2. Intelligente Inhalts-Filter
- Implementierung einer automatischen Blacklist für störende Dateien (Captcha-Bilder, Thumbnails, 'AL_Cave' Fragmente).
- Keine "Geister-Einträge" mehr in der Bibliothek durch systemgenerierte Dateien.

### 3. Dynamische UI
- Die Versionsanzeige im Footer und im "Über"-Dialog wird nun dynamisch vom Backend (v1.1.10) gespeist.
- Verfeinerte Kategorisierung: Automatische Unterscheidung zwischen *Album*, *Single* und *Compilation* (Various Artists).
- Ausblendung generischer Kategorien in der Listenansicht für ein cleaner Look.

### 4. Troubleshooting Support
- Dokumentierte Reset-Prozedur für Benutzer, die von manuellen Installationen auf das `.deb` Paket umsteigen.
- Korrektur des Logging-Verhaltens: Debug-Meldungen wie `[DB-Insert]` sind nun standardmäßig deaktiviert und über Flags steuerbar.

## Nächste Schritte
- Überwachung der Performance bei extrem großen Musikbibliotheken (> 50.000 Titel).
- Optionale Erweiterung des Video-Supports.

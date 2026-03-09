<!-- Category: Development -->
<!-- Title_DE: 04 Format-Vielfalt: ALAC, M4A & Co. -->
<!-- Title_EN: 04 Format Diversity: ALAC, M4A & More -->
<!-- Summary_DE: Erweiterung des Players um Unterstützung für verlustfreie und moderne Formate. -->
<!-- Summary_EN: Expanding the player to support lossless and modern formats. -->
<!-- Status: COMPLETED -->

# 04 Format-Vielfalt: ALAC, M4A & Co.

Ein einfacher MP3-Player reicht nicht aus, wenn man eine hochwertige Musiksammlung verwaltet. Die nächste Stufe der Komplexität war die Unterstützung von Formaten, die jenseits des Standards liegen (Commit `2e020a9`).

### Fokus auf Qualität
Besonderes Augenmerk lag auf **ALAC (Apple Lossless)** und dem **M4A/M4B Container**. 
- **Herausforderung:** Browser unterstützen ALAC oft nicht nativ.
- **Lösung:** Erste Überlegungen zur Identifizierung dieser Formate im Backend, um sie später durch Transcoding für den Browser verdaubar zu machen.

### Was wir gelernt haben
Das Hinzufügen neuer Formate zeigte schnell, dass eine reine Dateiendungs-Prüfung zu kurz greift. Es legte den Grundstein für die spätere, wesentlich komplexere **Metadaten-Pipeline** (Entry 05), die tief in die Header der Dateien schaut, um den echten Codec zu bestimmen.

<!-- lang-split -->

# 04 Format Diversity: ALAC, M4A & More

A simple MP3 player isn't enough when managing a high-quality music collection. The next level of complexity was supporting formats that go beyond the standard (Commit `2e020a9`).

### Focus on Quality
Special attention was given to **ALAC (Apple Lossless)** and the **M4A/M4B container**. 
- **Challenge:** Browsers often do not support ALAC natively.
- **Solution:** Initial considerations for identifying these formats in the backend to later make them digestible for the browser through transcoding.

### What we learned
Adding new formats quickly showed that a simple file extension check is insufficient. It laid the foundation for the later, much more complex **metadata pipeline** (Entry 05), which looks deep into file headers to determine the real codec.

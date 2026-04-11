# Imports für Buch-Inventur: Dokumentation

## Übersicht
Diese Imports ermöglichen eine vollständige, hybride Buch-Inventur mit Barcode- und OCR-Scanning, Metadaten-Erkennung und Realtime-Datenbank-Integration.

---

## Import-Liste
```python
import cv2                  # OpenCV: Webcam, Bildverarbeitung
import pyzbar.pyzbar as pyzbar  # pyzbar: Barcode/ISBN-Scan
import easyocr             # EasyOCR: Texterkennung (Titel/Autor)
import isbnlib             # isbnlib: ISBN-Validierung, Metadaten (offline/online)
from supabase import Client # Supabase: Realtime-DB für Inventur
from PIL import Image      # Pillow: Bildvorverarbeitung, Formatkonvertierung
import numpy as np         # NumPy: Array-Operationen für Bilddaten
```

---

## Zweck der einzelnen Imports
- **cv2 (OpenCV):**
  - Zugriff auf Webcam
  - Bildaufnahme und Vorverarbeitung (Graustufen, Kontrast, Threshold)
- **pyzbar:**
  - Dekodiert Barcodes (ISBN) aus Bildern/Webcam-Frames
- **easyocr:**
  - OCR für Titel/Autor vom Buchumschlag oder Rücken
  - Mehrsprachig (z.B. Deutsch/Englisch)
- **isbnlib:**
  - Validiert und standardisiert ISBN
  - Holt Metadaten (Titel, Autor, Verlag) offline/online
- **supabase:**
  - Speicherung und Realtime-Sync der Inventur-Daten
  - Integration mit NiceGUI für Live-Grid
- **PIL (Pillow):**
  - Bildkonvertierung, Vorverarbeitung für OCR
- **numpy:**
  - Effiziente Array-Operationen für Bilddaten

---

## Workflow mit diesen Imports
1. **Bild aufnehmen** (cv2)
2. **Barcode dekodieren** (pyzbar)
3. **OCR für Text** (easyocr)
4. **Metadaten ergänzen** (isbnlib)
5. **Daten speichern** (supabase)
6. **Vorverarbeitung** (PIL, numpy)

---

## Beispiel
```python
frame = cv2.VideoCapture(0).read()[1]
barcodes = pyzbar.decode(frame)
results = easyocr.Reader(['de', 'en']).readtext(frame)
meta = isbnlib.meta(isbn)
client = Client(SUPABASE_URL, SUPABASE_KEY)
client.table('physical_books').upsert(book).execute()
```

---

**Hinweis:**
- Alle Imports sind für die Inventur-Workflows in logbuch/OCR_Book_Scanner_Best_Practices.md und logbuch/Aufnahme_Buch_Inventur.md relevant.
- Für optimale OCR-Genauigkeit: Bildvorverarbeitung mit cv2, PIL, numpy.

---

**Frage:**
Benötigen Sie weitere Beispiele für die Nutzung dieser Imports im Inventur-Workflow?

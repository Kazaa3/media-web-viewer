# Logbuch: ODF-Integration Media-Library

## Datum: 10. März 2026

---

## Thema: odfpy vs. odfdo – Integration für Media-Library

### Vergleich
- odfpy: Basis-Library, XML-orientiert, stabil, klein
- odfdo: Moderne OOP-Library, einfachere API, aktiv, bessere Doku
- Empfehlung: odfdo für Media-Library, odfpy als Fallback

---

### Integration-Workflow
1. **Installieren:**
   - `pip install odfdo supabase`
2. **Datei verarbeiten:**
   - Metadaten, Volltext, Tabellen extrahieren
   - Daten in Supabase speichern
3. **Batch-Import:**
   - Alle ODF-Dateien aus Ordner verarbeiten
4. **Fallback:**
   - Bei Spezialfällen odfpy nutzen

---

### Codebeispiel (odfdo)
```python
from odfdo import Document
from supabase import Client
client = Client(SUPABASE_URL, SUPABASE_KEY)

def process_odf_file(odf_path):
    doc = Document(odf_path)
    meta = doc.meta
    data = {
        'path': str(odf_path),
        'type': 'odf',
        'format': odf_path.suffix,
        'title': meta.title or 'Unbekannt',
        'creator': meta.initial_creator or 'Unbekannt',
        'text_preview': doc.full_text()[:1000],
    }
    client.table('media').upsert(data).execute()
    print(f"✅ {data['title']} verarbeitet!")
```

---

### Use-Cases
- .odt: Reports, Notizen → Text-Suche
- .ods: Tabellen → Pandas Import
- Inventur: Scan + ODF Meta validieren

---

### Fazit
- odfdo ist für Media-Library-Integration einfacher und moderner.
- odfpy bleibt als XML-Fallback verfügbar.
- Supabase ermöglicht Realtime-Sync und Batch-Import.

---

**Nächste Schritte:**
- Test: .odt laden → Supabase
- NiceGUI-Integration für Upload und Vorschau
- OCR-Kombination für Umschlag + ODF-Metadaten

---

**Fragen/Feedback:**
- Weitere Beispiele oder Integrationswünsche?

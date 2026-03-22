# ODF-Formate: odfpy vs. odfdo

## Übersicht
Für die Verarbeitung von OpenDocument-Formaten (ODT, ODS, OTP, ODP) gibt es zwei etablierte Python-Libraries: **odfpy** und **odfdo**. Beide bieten Zugriff auf Text, Tabellen und Metadaten, unterscheiden sich aber in API und Features.

---

## odfpy
- **Installation:**
  ```bash
  pip install odfpy
  ```
- **Features:**
  - Lesen/Schreiben von ODT, ODS, ODP, OTP
  - Zugriff auf XML-Struktur, Metadaten, Text
  - API: Low-Level, XML-basiert
- **Beispiel:**
  ```python
  from odf.opendocument import load
  doc = load('test.odt')
  print(doc.meta.title)
  print(doc.text.get_text())
  ```

---

## odfdo
- **Installation:**
  ```bash
  pip install odfdo
  ```
- **Features:**
  - Lesen/Schreiben von ODT, ODS, ODP, OTP
  - High-Level API für Text, Tabellen, Metadaten
  - Einfaches Extrahieren und Modifizieren von Inhalten
- **Beispiel:**
  ```python
  from odfdo import Document
  doc = Document.load('test.odt')
  print(doc.get_meta('title'))
  print(doc.text())
  ```

---

## Vergleich
| Feature         | odfpy           | odfdo           |
|----------------|-----------------|-----------------|
| API            | Low-Level XML    | High-Level      |
| Metadaten      | Ja               | Ja              |
| Text extrahieren| Ja              | Ja              |
| Tabellen       | Ja               | Ja              |
| Modifizieren   | Ja (komplizierter)| Ja (einfach)    |
| Performance    | Schnell          | Schnell         |
| Community      | Aktiv            | Aktiv           |

---

## Empfehlung
- **odfpy:** Für komplexe XML-Manipulationen und volle Kontrolle.
- **odfdo:** Für schnelle, einfache Extraktion und Modifikation von Text/Tabellen.

---

**Frage:**
Welche Library möchtest du für deine ODF-Workflows nutzen? Beide sind kompatibel mit ODT, ODS, OTP, ODP.

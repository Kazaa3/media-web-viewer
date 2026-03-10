<!-- Status: ACTIVE -->
date: 2026-03-10
category: parser
tags: [parser, iso, bin, img, differentiation, cd-rom, dvd]

# Logbuch-Eintrag: Differenzierung von Disk-Abbildern (CD vs. DVD)

## Übersicht

Mit der Hinzufügung neuer Medientypen (PC-Spiele auf CD, Buchbeilagen) wurde deutlich, dass eine pauschale Bezeichnung als "Abbild" oder "ISO" nicht ausreicht. Die Parser-Logik wurde erweitert, um zwischen CD-ROM, DVD und Blu-ray Abbildern zu unterscheiden.

## Neue unterstützte Formate

Zusätzlich zu `.iso` werden nun folgende Formate in der Parser-Chain und im Mapping unterstützt:
- **.bin / .cue:** Typisch für Mixed-Mode CDs oder ältere PC-Spiele.
- **.img:** Allgemeines Disk-Abbild.
- **.nrg / .mdf:** (Vorbereitet) Proprietäre Formate.

## Differenzierungs-Logik (Heuristiken)

Da Metadaten (Volume-ID) nicht immer sofort verfügbar oder lesbar sind (siehe Probleme mit `pycdlib` bei UDF), wurden in `format_utils.py` größenbasierte Heuristiken implementiert:

| Größe | Erkannter Typ |
| :--- | :--- |
| < 100 MB | Disk-Abbild (Allgemein) |
| 100 MB - 1 GB | CD-ROM (Abbild) |
| 1 GB - 9 GB | DVD (Abbild) |
| > 9 GB | Blu-ray (Abbild) |

**Priorität:** Wenn Metadaten (z.B. "PAL", "DVD VIDEO", "SACD") in den Tags gefunden werden, überschreiben diese die Größen-Heuristik.

## Verifizierung und Tests

Ein neuer Test `tests/test_image_differentiation.py` verifiziert die korrekte Benennung der neuen Samples:
- `S3gold1_g.bin` (735MB) -> **CD-ROM (Abbild)**
- `1411_c_von_a_bis.iso` (134MB) -> **CD-ROM (Abbild)**
- `4_KOENIGE.iso` (6.8GB) -> **DVD (Abbild)**
- `Going Raw - JUDITA_169_OPTION.ISO` (1.2GB) -> **DVD (Abbild)**
- `OLE_DB_ODBC.iso` (24MB) -> **Disk-Abbild**

## Fazit

Diese feingranulare Unterscheidung verbessert die Benutzererfahrung in der GUI, da der Anwender sofort sieht, ob es sich um eine CD-Beilage oder einen Spielfilm handelt, noch bevor der volle Scan abgeschlossen ist.

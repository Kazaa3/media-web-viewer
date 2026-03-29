# Logbuch: RequestsDependencyWarning (urllib3/chardet/charset_normalizer)

## Problem
- Beim Import oder der Nutzung von `requests` erscheint folgende Warnung:
  ```
  RequestsDependencyWarning: urllib3 (2.2.3) or chardet (7.1.0)/charset_normalizer (3.3.2) doesn't match a supported version!
  ```
- Ursache: Die installierten Versionen von `urllib3`, `chardet` oder `charset_normalizer` sind nicht mit der von `requests` unterstützten Version kompatibel.

## Auswirkungen
- Es handelt sich um eine Warnung, kein harter Fehler – Requests funktioniert meist trotzdem, aber es kann zu unerwartetem Verhalten kommen.
- Besonders relevant in Umgebungen mit Anaconda oder gemischten Paketquellen.

## Lösung
- Kompatible Versionen installieren:
  ```bash
  pip install 'requests>=2.28,<2.32' 'urllib3>=1.21.1,<2.0' 'chardet<5' 'charset_normalizer<4'
  ```
- Alternativ: In der Umgebung gezielt die Versionen anpassen, z.B. mit conda oder pip.
- Nach der Anpassung: Warnung sollte verschwinden.

## Status 15.03.2026
- Die Warnung wurde untersucht, aber noch nicht dauerhaft gefixt.
- Es wurden die empfohlenen Versionen von requests, urllib3, chardet und charset_normalizer installiert.
- Die Warnung sollte damit verschwinden, ist aber noch zu beobachten.
- Weitere Tests und ggf. Anpassungen in requirements/environment.yml sind empfohlen, um die Kompatibilität langfristig sicherzustellen.

## Hinweise
- Die Warnung kann ignoriert werden, solange keine Fehler auftreten – empfohlen wird aber die Anpassung für maximale Kompatibilität.
- In CI/CD-Umgebungen auf konsistente requirements achten.

---

**Siehe auch:**
- https://github.com/psf/requests/issues/6432
- requirements.txt, environment.yml

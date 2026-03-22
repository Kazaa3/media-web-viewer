# Hinweis: .venv_testbed als Referenz – .gitignore

**Datum:** 15.03.2026

## Empfehlung
- Die Referenz-Umgebung `.venv_testbed` dient ausschließlich als lokale Testumgebung und sollte **nicht** ins Git-Repository eingecheckt werden.
- Der Eintrag `.venv_testbed/` ist daher in der `.gitignore` zu hinterlegen, um versehentliche Commits zu vermeiden.

## Beispiel (.gitignore)
```
# Lokale Testumgebung
.venv_testbed/
```

## Ergebnis
- Die Testumgebung bleibt lokal, das Repository bleibt sauber und portabel.

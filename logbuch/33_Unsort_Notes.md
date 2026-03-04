<!-- Category: Planung -->

Recap der Änderungen
Footer: Der Player-Footer ist nun in allen Tabs (Player, Bibliothek, Browser, etc.) permanent sichtbar. Die Logik, die ihn im Bibliotheks-Tab ausgeblendet hat, wurde entfernt.
Indexing:
Die Anwendung nutzt nun absolute Pfade für den Scan (.resolve()), was Fehler bei relativen Pfaden verhindert.
Beim Start der App wird automatisch ein Scan des 
media/
-Ordners durchgeführt.
Detaillierte Log-Ausgaben im Terminal zeigen nun genau an, welcher Pfad gescannt wird ([Scan] Starting scan of: ...).
Verifizierte Funktionen
 Footer bleibt beim Wechsel in den "Bibliothek"-Tab sichtbar.
 Initialer Scan beim Start verarbeitet die Dateien im Projekt-Ordner 
media/
.
 Terminal-Logs bestätigen den korrekten Scan-Pfad.
 
 
 

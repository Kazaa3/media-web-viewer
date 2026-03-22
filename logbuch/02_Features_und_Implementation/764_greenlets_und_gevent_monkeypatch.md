# Greenlets und gevent.monkey.patch_all() in Eel-Apps

## Was sind Greenlets?
Greenlets sind leichte, kooperative „Threads“ in Python, die in einem einzigen nativen OS‑Thread laufen und nicht vom Kernel, sondern vom Laufzeitsystem (z.B. gevent oder der greenlet‑Bibliothek) verwaltet werden.

**Technischer Hintergrund:**
- Greenlets sind Coroutinen auf Basis des C‑Moduls `greenlet`.
- Sie erlauben, zwischen verschiedenen Funktions‑„Stacks“ hin‑ und herzuwechseln, ohne dass der Kernel involviert ist.
- Im Gegensatz zu echten Threads wählt bei Greenlets das Programm selbst, wann geswitcht wird (kooperativ), statt dass der Kernel jederzeit unterbrechen kann (präemptiv).

**Eigenschaften:**
- Sehr leichtgewichtig: Viele hundert oder tausende Greenlets pro Prozess möglich, mit geringem Speicherbedarf.
- Single Thread: Alle Greenlets laufen im selben OS‑Thread, keine echte Parallelität auf mehreren CPU-Kernen.
- Ideal für I/O‑bound‑Lasten (HTTP‑Requests, Sockets, Datenbank‑Calls), bei denen oft gewartet wird.

**Beispiel mit gevent:**
```python
import gevent

def worker(n):
    print(f"Worker {n} start")
    gevent.sleep(1)   # explizites „yield“ (Greenlet gibt Kontrolle explizit ab, damit andere Greenlets laufen können)
    print(f"Worker {n} stop")

# 3 Greenlets starten
jobs = [gevent.spawn(worker, i) for i in range(3)]
gevent.joinall(jobs)   # bis alle fertig sind
```
Hier laufen 3 worker‑Funktionen „gleichzeitig“, aber in einem einzigen Thread – sie wechseln beim Aufruf von gevent.sleep oder bei anderen I/O‑Operationen explizit.

---

## Was macht gevent.monkey.patch_all() in einer Eel-App?

Kurz gesagt: `gevent.monkey.patch_all()` ersetzt in deinem Prozess zentrale Blocking-APIs (Sockets, Threads, teilweise time, subprocess etc.) durch gevent‑Versionen, damit diese kooperativ arbeiten und sich Greenlets statt „echter“ Threads/Sockets verwenden lassen.

**Was macht der Monkey Patch technisch?**
- Er „patcht“ Standardbibliothek‑Module wie socket, thread, threading, time, ggf. subprocess, so dass Aufrufe intern über gevent laufen.
- Blockierende Operationen wie Netzwerk‑I/O blockieren dann nur das jeweilige Greenlet, nicht den ganzen Prozess, solange du in einem gevent‑Kontext (z.B. via gevent.spawn) arbeitest.
- Optional kann auch threading so gepatcht werden, dass threading.Thread effektiv Greenlets statt OS‑Threads nutzt.

**Beispiel (vereinfachtes Prinzip):**
```python
from gevent import monkey
monkey.patch_all()

import socket  # ist jetzt die gevent-kompatible Variante
```

**Speziell in einer Eel‑App:**
- Eel selbst basiert (je nach Version/Fork) typischerweise auf gevent/gevent‑websocket oder einem anderen Server; bei gevent musst du das Monkey‑Patching explizit vor dem Import von Eel machen, wenn du es überhaupt brauchst.
- Sinnvoll ist das insbesondere, wenn du in deinem Backend viel Netzwerk‑I/O, HTTP‑Calls, Datenbank‑Clients etc. hast und diese kooperativ parallelisieren willst, ohne deine ganze Logik auf gevent umzuschreiben.

**Nebenwirkungen / Stolpersteine:**
- Das Verhalten von threading, socket usw. ist nicht mehr exakt das der CPython‑Stdlib; das kann zu schwer nachvollziehbaren Effekten führen, gerade bei bereits komplexem Code (viele Threads, Subprocess‑Nutzung, Tools wie VS Code Debugger).
- Wenn du ohnehin in deiner Eel‑App keinen bewussten gevent‑Code (Greenlets, gevent‑Server) nutzt, profitierst du u.U. kaum davon, hast aber das Risiko von „magischen“ Seiteneffekten.
- Debugger und manche Libraries können durch Monkey‑Patching irritiert werden, deshalb wird empfohlen, es nur zu nutzen, wenn du es wirklich brauchst und es so früh wie möglich im Prozess auszuführen (ganz am Anfang von main.py).

---

*Logbuch-Eintrag erstellt: 20. März 2026*
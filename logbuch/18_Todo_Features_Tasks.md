<!-- Category: Planung -->

# Todo


## Funktionen
# File-Handling
# - Medien scannen (Ordner durchsuchen, Metadaten extrahieren)
# - Weitere Funktionen hinzufügen, z.B. zum Abspielen von Medien, Verwalten von Wiedergabelisten, etc.


##### GUI
# - Hauptfenster mit Navigation (Medienbibliothek, Wiedergabelisten, Einstellungen)
# - Medienbibliothek (Datei-Explorer, Drag & Drop)


##### Datenbank
# Wechsel zu:  pywebview oder Flask
# SQLite über sqlite3 oder SQLAlchemy


############ Datenmodel
# Datenstruktur für Medien
# class MediaItem(name, path, type, duration, tags, ...)

# Parser zusammen führen
# Duplikat-Erkennung

# logische trennung item / full object mit allen tags
#Parser-Zeiten:
#pymediainfo: 2.2ms • mutagen: 0.4ms • container: 0.0ms • filename: 0.0ms • ffmpeg: 51.0ms
#neu sortieren 1.filename 2.container 3. mutagen 4. pymediainfo 5. ffmpeg
# kapitel parser für 3 und 4
# string parser: wenn "zahl " vor dem Titel steht, dann ist das die Tracknummer, z.B. "02 Ludwig van Beethoven" --> Track 2
# container auslesen. mkv parsing. mkv hat keine tags. mkv hat nur streams. 
# cointainer nested aac parsen



### SCAN Debugging-Logs unvollständig bzw sind die einzigen




#
#
# Flags Popup Bug

# m4b sind Hörbücher
# mkv audio. if no video
# mkv video, wenn min 1 video
# Hinter den Namen nicht Audio schrieben 

#20 in strings





# Test Kategorien
# Testframe work erklären
#pytest
#+ Selenium + Dom anweisungen
# Testnamen bearbeitbar machen
# Beschriebung hinzufügen
# Testeregbnisse die nötig für pass sind hinzufügen




# Feature Request Window
# Liste von allen Mini Features, sowie in Tasks.md und Walktrough. Alles resoren
#beim klciken der features soll sich ein log buch öffnen. wo jeder der punkte aus dem panel ausfürhlich behandelt wird mti eigener .md dort hin kopiert. der ordner heißt logbuch


# Chapter sorting rework

# Rework Logbook
# Feature Request
# Da drunter schon implementiert

# Namensdoument. footer / pop up synnyme
# Funktionsdokument. so wie read-me

# tut
# File format guides zru Erklärung
# json parsing dict
# technoligie möglichkeiten
# Einteilung wireframe, mockups, prototypes, UI, UX
# bze kurz, mittel, lang


# git
#Edit repository details
# Releases
# Branches
# Packages


# STelle merken
# Play count
# Last played
# Rating
# Vor und zurück
# Playlist
# Alben, Compilations, SSingles, etc.
# Filme und Serien
# Ebooks
# Bilder
# Dokumente
# Archive
# Sonstige
# Daten Typen, die noch zu identifizieren sind
# Test mit selenium
# Test mit pytest
# Vibecoding mit Antigravity

# Lernen JavaScript
# Refresh HTML, CSS
# Refresh Python
# Refresh EEL
# pYTHON Datenanalyse
# Python Scraping

### Typen erstellen


# Audio  --> Werte --> Bitrate --> Samplerate --> Bitdepth --> Tag-Format --> Container
# WMAV2  --> ASFTags --> ASF
# WAV24 --> PCM_S24LE | 32 Bit (s32) | 44.1 kHz
# WAV16 --> PCM_S16LE | 16 Bit (s16) | 44.1 kHz

#mp4a.40.2 | 16 Bit (lossy) | 44.1 kHz | 320 kbps
#149.86 MB • Art: Yes
#File: M4B • Container: m4a • Tag Format: MP4Tags
#PCM_S16LE | 16 Bit (s16) | 44.1 kHz | 1411 kbps
#79.21 MB • Art: No
#File: wav • Container: wave
#Parser-Zeiten:
#pymediainfo: 10.0ms • mutagen: 0.3ms • container: übersprungen • filename: 0.0ms • ffmpeg: übersprungen
#die unetrkapitelsortierung ist nicht 1,2,3 sondern 1,21,22,2
# # debug flags menu
# mandatory unit test for all new components
# agenten gesteuerter browser test
# m4b sind immer hörbücher und nicht audio
#die unetrkapitelsortierung ist nicht 1,2,3 sondern 1,21,22,2
# alte einträge zu typ, container und tag ist weg und soll wieder in das linke seiten fenster des players
# tESTS IMMER hinzufügen
# kommentare hinzufügen für doku ki komen

#mkvinfo
#mediainfo
#mp3tag
# Untersützedateiformate als Liste

# Tags
# ID3v2.4 / ID3v2.3 / ID3v2.2 / ID3v1.1 / ID3v1
# APEv2 / APEv1
# MP4 Atoms
# FLACVComment
# OggVComment

# weitere Container
# mp4, avi, mov, mkv, webm, flv, wmv, mpg, mpeg, m4v, 3gp, 3g2, ogv, ogg, mts, m2ts

#Dokumente
# pdf, doc, docx, txt, md, html, htm
# epub, mobi, azw, fb2

# sonstige
# zip, rar, 7z, tar, gz, bz2, xz
# exe, dmg, deb, rpm, apk
# iso, img, vhd, vmdk, vdi
# bat, sh, ps1, cmd
# py, js, html, css, php, java, c, cpp, h, hpp, cs, rb, go, rs, swift, kt,kts,kts


                    # ==========================================
                    # CONTAINER-FORMAT AUSWERTUNG (FFmpeg)
                    # ==========================================
                    # FFmpeg gibt in der Line "Input #0" das exakte Demuxer-Format an.
                    # Viele Formate teilen sich historisch denselben Container-Standard:
                    # 
                    # 1. ISOBMFF (Apple QuickTime Derivate):
                    #    Formate wie .mp4, .m4a (Audio) und .m4b (Audiobooks) basieren alle 
                    #    auf dem "Base Media" Format (ISO/IEC 14496-12). FFmpeg fasst diese 
                    #    beim Einlesen generisch unter dem Begriff "mov,mp4,m4a,3gp,3g2,mj2" zusammen.
                    #    Wenn wir "MOV" auslesen, aber die Datei eigentlich ".m4b" heißt, 
                    #    korrigieren wir die Anzeige für den User exakt auf die Dateiendung (z.B. M4B).
                    #
                    # 2. Matroska / WebM:
                    #    Ein extrem flexibler Open-Source Container, der fast alle Streams schluckt.
                    #    FFmpeg meldet hier "matroska,webm". Wir bereinigen das visuell zu "MKV".
                    # ==========================================

            # ==========================================
            # AUDIO-TAG AUSWERTUNG (Mutagen)
            # ==========================================
            # Je nach Dateityp verwendet die Mutagen-Bibliothek völlig unterschiedliche Parser.
            # Um dem Nutzer saubere, branchenübliche Tag-Typen anzuzeigen, schlüsseln wir diese auf:
            #
            # 1. ID3 (MP3):
            #    ID3-Tags haben historisch viele Iterationen (v1, v2.2, v2.3, v2.4). Da die Version hier
            #    elementar für die Kompatibilität von Car-Audios und Playern ist, lesen wir explizit
            #    den `tags.version` Tuple (z.B. (2,3,0)) aus und wandeln ihn formal in "ID3v2.3" um.
            # 
            # 2. ISOBMFF / Apple (MP4/M4A/M4B):
            #    Nutzt intern sogenannte "MP4 Atoms" (ilst). Ein versionierungsgeladenes Chaos 
            #    wie bei ID3 gibt es hier nicht. Wir benennen Mutagens rohes "MP4Tags" in das
            #    cleane "MP4" um.
            #
            # 3. Xiph (Ogg/FLAC):
            #    Nutzen den "Vorbis Comment" Standard (eine simple LISTE von Schlüssel=Wert paaren).
            #    Auch hier gibt es keine nennenswerte Unterversionierung. Um sie voneinander 
            #    zu trennen, benennen wir "OggVComment" und "FLACVComment" in menschliche Strings um.
            # ==========================================




# MediaItem logic moved to models.py
# test aktulisierung unten rechts
# aletr lösch button
# Flags steuerung rework
# Konsole wird teils zu gespammt 
# im anderen fall nicht genug infos
# merken der standard einstellung und reihenfolge

##Erjlären
# Daten model
# File typen
# Container
# Codec
# Bit depth
# Sampling rate
# Bitrate
# Channels
# Duration
# File size
# Cover art
# Chapters
# Tags
# Parser
# Transcoding
# Cache
# Debug
# Walkthrough
# Tasks
# Feature Request
# Logbook
# Namensdocument
# Funktionsdokument
# File format guides
# gui
# selen etsting
# py testing

#unetrschiede bei alac, bei mp3
#/media/01-05-Joan_Baez-Lowlands-LLS.m4a.flac_transcoded
# /media/02%20Ludwig%20van%20Beethoven%20-%20Piano%20Concerto%20No.%205%20in%20E-flat%20major%2C%20Op.%2073%20''Emperor''-%20II.%20Adagio%20un%20poco%20mosso.wav

# Testdaten generell


# Testdateien Ordner mit infos
# m4b mit Cahpetr Variante 1
# m4b mit variante 2
# späetr dokumente: pdf

# Benchmarking
# Parsen, Sorting, Einlesen, Unterschiedliche PArser, Transkodierung, Cache



#requriements.txt
# env
# alle alten .md in das logbuch kopieren


# datenbank logik
# wie werden items angelegt.
# für jeden medientp eigene daten bank
# felder für unterschiedlice tags unetrschiedlich.
# trotzdem eine große datenbank


# Anforderungen. Neue Features
# Bestehende Features
# Zu erweiternde Features
# 

# Benchmarking
# Parsen, Sorting, Einlesen, Unterschiedliche PArser, Transkodierung, Cache


# Werte auf GUI Qexposen
# Immer alle .md  und nach logbuch. walktrough, Scratchpad .mds geenrell

# git kommentare


#debug db
#debug parser
#debug transcoding
#debug cache
#debug gui
#debug selen etsting
#debug py testing

#zu db
# datei auswählen. standard ist das dict
# konsole log doku
# 

# ganz ferne zukunft:
# web gui mit playlist
# ki sortierung
#

# oPTIONEN REWORK
# Neue anordnung
# Flagssteuerung ist doppelt, aber lassen weil es so gut funktioniert.
# lern tool einbauen mit puzzle




#gui element zentrierung
# diverses
# scrolbar abschalten
# Design Ideen für Rework


# Dateiendung änderbar machen



# universales Wörterbuch für Tags
# Berücksichtigung der unterschiedlichen TAg varianten

#smb / nfs / webdav / ftp / sftp

# screenshots

# kommentar rework

# Die vielen Pythons anschauen
# Linux 7 user / bin / home /ab / anaconda3 / envs / p14 / bin / python3.14
# conda env list
# conda activate p14
#global lokal
#/bin/python3.11


# fehlt test tab rework
# Testkategorien
# Eingabewerte
# Ausgabewerte
# Testdateien
# Aufzählung der passes
# Kommentar


# sprache, impressum, legende
# item, footer
# getrentn nach technologie
#decorator 

# notizbuch
# ausbauen


#eel
#http://localhost:8000/app.html
#selenium testing

# anderer port
#check für refresh, wenn down

# un abgehakte punkte wieder hinzufügen

# doku library
# mutagen
# ffmpeg
# parser
# db
# cache
# gui
# selenium
# py testing
#python
# eel
#mct

#rezepeti

#reiben in der app. nicht nur liste


# chore
# https://www.w3tutorials.net/blog/when-to-use-chore-as-type-of-commit-message/

#debug fenster:
# Erweiterung um andere DAteityen als das dict/json



# Läuft über Tkinter
# Kann man das auch über eel machen?
# Funktioniert der manuelle import mehrer dateien


# templates
# an gui schicken
# globale flanke
# tbc

#datenfluss diagram

# unetr feartures
# unten loogbuch link
# Synchronisiert mit `task.md` und `walkthrough.md` • Klicken für Details

#logbuch ist verloren gegangen. heir die .mds


# perplexity kopierer / scraper


# json.dumps() garantiert JSON-konforme double quotes und Escaping.

#rework. the dokmentation
#jede.md datei jeden implementation plan in logbuch speichern. 
#rename
#task.md
#walktrough.md
#implementationplan.md
#review changes
#sowie git kommentare


# CApture tool

# in dem feautres modal.... soll es unter: v den link zum vollständigen logbuch tab geben


# Einafches Logbuch mit modal
# Vollständiges Logbuch
# Erweitertes Logbuch mit Kategorieren
# Test cases mit KAtegorien

#Logbuch
# Einträge zu Feature
# Zwei Spalten
# unetre abgeschlossen Feature mit unerOrdner im logbuch
# unten rechts Impressum / gloassar
# bearbeiten buttton funktioniert nicht



#dokumentiere alle feature im logbuch


# Visuelles Redesign: Die einfache Checkbox-Liste wurde in ein "Rich Card"-Layout übersetzt
#die doku im logbuch erneuern


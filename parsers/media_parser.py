import time
from pathlib import Path
from . import filename_parser
from . import mutagen_parser
from . import pymediainfo_parser
from . import ffmpeg_parser

def extract_metadata(path, filename, debug=False):
    """
    Zentraler Parser, der Redundanzen vermeidet und FFmpeg-Subprozesse
    für die Indexierung überflüssig macht.
    """
    if debug:
        print(f"[Debug-Parser] Starte Parsing für: {filename}")
        
    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    
    # 1. Basis-Tags aus Dateiname generieren
    tags = filename_parser.parse(path_obj, filename)
    
    # 2. Mutagen (schnell, nativ in Python)
    tags = mutagen_parser.parse(path_obj, file_type, tags, filename)
    
    duration = 0
    # Mutagen liefert bei einigen Formaten keine Dauer mehr zurück 
    # (weil wir _get_duration() aus main.py konsolidiert haben).
    # Deswegen holen wir hier die Dauer direkt mit ab, falls Mutagen
    # sie in mutagen_parser.py nicht schon integriert hat.
    # Da mutagen_parser.py momentan nur Tags liefert, lassen wir
    # pymediainfo_parser auch die Duration auslesen.
    
    # Prüfen, ob wichtige Info fehlt (Dauer, Samplerate, Bitrate, Codec, Bitdepth)
    needs_fallback = (
        not tags.get('samplerate') or 
        not tags.get('bitrate') or 
        not tags.get('bitdepth') or
        not tags.get('duration') or
        tags.get('tagtype') == 'None'
    )
    
    if needs_fallback:
        # 3. Pymediainfo Fallback (schnelles C-Binding, kein Subprozess!)
        tags = pymediainfo_parser.parse(path_obj, file_type, tags)
    
    # Dauer aus den Tags extrahieren und standardisieren
    if 'duration' in tags and tags['duration']:
        try:
            duration = int(tags['duration'])
        except (ValueError, TypeError):
            duration = 0
    # 4. FFmpeg Fallback für fehlende Werte (insbesondere Float-Bitdepth bei Lossy)
    # Deaktiviert standardmäßig, da es einen ressourcenintensiven Subprozess startet.
    # Wenn gewünscht, kann dies über einen optionalen Parameter injiziert werden,
    # aber wir vermeiden hier den direkten Import von `main.py`, um zirkuläre
    # Abhängigkeiten (ImportError) zu verhindern!
    
    needs_ffmpeg = (
        not tags.get('samplerate') or 
        not tags.get('bitrate') or 
        not tags.get('bitdepth') or
        not duration
    )
    if needs_ffmpeg and False:
        tags = ffmpeg_parser.parse(path_obj, file_type, tags)
        if not duration and tags.get('duration'):
            try:
                duration = int(tags['duration'])
            except (ValueError, TypeError):
                duration = 0
                
    # 5. Final Fallback for Lossy / Missing Bitdepth
    # The user specifically requested formats like MP3 to default to "16 Bit (lossy)"
    # if no bit depth was extracted natively by the parsers.
    if not tags.get('bitdepth'):
        lossy_extensions = {'.mp3', '.ogg', '.aac', '.m4a', '.m4b', '.wma', '.opus'}
        if file_type in lossy_extensions:
            tags['bitdepth'] = "16 Bit (lossy)"
        else:
            tags['bitdepth'] = "16 Bit"
            
    return duration, tags

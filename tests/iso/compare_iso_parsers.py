#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: ISO / Parser / Vergleich
# Eingabewerte: media/4 Könige (2015) - DVD/4_KOENIGE.iso, pycdlib, isoparser
# Ausgabewerte: Vergleich der Parser-Ergebnisse und Performance
# Testdateien: media/4 Könige (2015) - DVD/4_KOENIGE.iso
# ERWEITERUNGEN (TODO): [ ] Erweiterung auf weitere ISO-Parser, [ ] Performance-Optimierung
# KOMMENTAR: Vergleicht pycdlib und isoparser für ISO-Parsing.
# VERWENDUNG: python3 tests/iso/compare_iso_parsers.py
import os
import time
from pathlib import Path

try:
    import pycdlib
    HAS_PYCDLIB = True
except ImportError:
    HAS_PYCDLIB = False

try:
    import isoparser
    HAS_ISOPARSER = True
except ImportError:
    HAS_ISOPARSER = False

SAMPLE_ISO = "./media/4 Könige (2015) - DVD/4_KOENIGE.iso"

def compare_parsers():
    """
    Vergleicht pycdlib und isoparser für ISO-Parsing. / Compares pycdlib and isoparser for ISO parsing.

    Returns:
        None
    """
    if not os.path.exists(SAMPLE_ISO):
        print(f"Error: Sample ISO not found at {SAMPLE_ISO}")
        return

    print(f"Comparing ISO Parsers for: {SAMPLE_ISO}\n")

    # 1. Test pycdlib
    if HAS_PYCDLIB:
        print("--- Testing pycdlib ---")
        start = time.time()
        try:
            iso = pycdlib.PyCdlib()
            iso.open(SAMPLE_ISO)
            vol_id = iso.get_volume_id().decode('utf-8', 'ignore').strip()
            total_files = len(iso.list_children(iso_path='/'))
            iso.close()
            print(f"Result: SUCCESS")
            print(f"Volume ID: {vol_id}")
            print(f"Root Files Count: {total_files}")
        except Exception as e:
            print(f"Result: FAILED - {e}")
        end = time.time()
        print(f"Duration: {end - start:.4f}s\n")
    else:
        print("pycdlib not installed.\n")

    # 2. Test isoparser
    if HAS_ISOPARSER:
        print("--- Testing isoparser ---")
        start = time.time()
        try:
            iso = isoparser.parse(SAMPLE_ISO)
            vol_label = "Unknown"
            if hasattr(iso, 'volume_descriptors') and 'primary' in iso.volume_descriptors:
                pvd = iso.volume_descriptors['primary']
                vol_label = getattr(pvd, 'volume_id', getattr(pvd, 'volume_identifier', 'Unknown'))
            
            total_files = len(list(iso.root.children)) if hasattr(iso, 'root') else 0
            print(f"Result: SUCCESS")
            print(f"Volume Label: {vol_label}")
            print(f"Root Files Count: {total_files}")
        except Exception as e:
            print(f"Result: FAILED - {e}")
        end = time.time()
        print(f"Duration: {end - start:.4f}s\n")
    else:
        print("isoparser not installed.\n")

if __name__ == "__main__":
    compare_parsers()

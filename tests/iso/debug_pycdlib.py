import pycdlib
import struct
import traceback

SAMPLE_ISO = "./media/4 Könige (2015) - DVD/4_KOENIGE.iso"

def debug_pycdlib():
    print(f"Debugging pycdlib open for: {SAMPLE_ISO}")
    iso = pycdlib.PyCdlib()
    try:
        # Manually try to read the first few blocks to see if it's readable
        with open(SAMPLE_ISO, 'rb') as f:
            # ISO 9660 starts with 32KB of system area (zeros)
            # Volume descriptor starts at 32KB (offset 32768)
            f.seek(32768)
            header = f.read(2048)
            print(f"Header at 32KB length: {len(header)}")
            if len(header) > 0:
                print(f"Header bytes (first 16): {header[:16].hex()}")
            
        iso.open(SAMPLE_ISO)
        print("Success!")
    except Exception as e:
        print(f"Failed with error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_pycdlib()

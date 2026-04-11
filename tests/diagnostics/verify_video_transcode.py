import requests
import time
import sys
import traceback

# --- CONFIGURATION ---
BASE_URL = "http://localhost:8345"
TEST_ITEM_PATH = "Set It Off (1996) - Director's Cut - PAL.mkv"
# Test BOTH remux and transcode endpoints
ENDPOINTS = [
    f"{BASE_URL}/video-remux-stream/{requests.utils.quote(TEST_ITEM_PATH)}",
    f"{BASE_URL}/stream/via/transcode/{requests.utils.quote(TEST_ITEM_PATH)}"
]

def verify_streaming():
    overall_success = True
    
    for url in ENDPOINTS:
        print(f"\n🚀 [Diagnostic] Testing endpoint: {url}")
        try:
            # 1. Start a streaming request
            response = requests.get(url, stream=True, timeout=10)
            
            print(f"📡 Status: {response.status_code}")
            print(f"📝 Content-Type: {response.headers.get('Content-Type')}")

            if response.status_code != 200:
                print(f"❌ [FAILURE] Server error {response.status_code}")
                overall_success = False
                continue

            # 2. Verify Data Flow and Header
            print(f"Wait for first chunk...")
            iterator = response.iter_content(chunk_size=512 * 1024)
            try:
                chunk = next(iterator)
                print(f"📦 Received {len(chunk)} bytes.")
                
                # Check for MP4 magic atoms: ftyp, moof, mdat, moov
                atoms = [b'ftyp', b'moof', b'mdat', b'moov', b'free', b'skip']
                found = [atom.decode() for atom in atoms if atom in chunk[:2048]]
                
                if found:
                    print(f"✅ [SUCCESS] MP4 atoms detected: {', '.join(found)}")
                else:
                    print(f"❌ [FAILURE] No valid MP4 atoms in start of stream.")
                    print(f"🔍 [Debug] Hex dump (start): {chunk[:32].hex()}")
                    overall_success = False
                
                # Try reading one more chunk to ensure the process didn't crash
                next_chunk = next(iterator)
                print(f"✅ [SUCCESS] Continuous flow: {len(next_chunk)} bytes.")

            except StopIteration:
                print(f"❌ [FAILURE] Stream ended immediately.")
                overall_success = False
            except Exception as e:
                print(f"❌ [FAILURE] Error during read: {e}")
                overall_success = False
            
            response.close()

        except Exception as e:
            print(f"❌ [FAILURE] Connection error or timeout: {url}")
            overall_success = False

    if overall_success:
        print("\n🏁 [FINAL RESULT] All video streaming pipelines are OPERATIONAL.")
        sys.exit(0)
    else:
        print("\n🏁 [FINAL RESULT] Some pipelines remain BROKEN.")
        sys.exit(1)

if __name__ == "__main__":
    verify_streaming()

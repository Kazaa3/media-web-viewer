import subprocess, re
out = subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1", "-c:a", "libmp3lame", "-b:a", "128k", "test.mkv"], stderr=subprocess.PIPE, text=True).stderr
out = subprocess.run(["ffmpeg", "-i", "test.mkv"], stderr=subprocess.PIPE, text=True).stderr
for line in out.splitlines():
    if "Stream #0" in line:
        print(line)
        audio_line = re.search(r"Stream #.*?: Audio:(.*)", line)
        if audio_line:
            al = audio_line.group(1)
            br_match = re.search(r"(\d+)\s*kb/s", al)
            print("Regex KB/s match:", br_match.group(1) if br_match else "NONE")
            
            bit_match = re.search(r"bitrate:\s*(\d+)\s*kb/s", out)
            print("Global bitrate match:", bit_match.group(1) if bit_match else "NONE")
subprocess.run(["rm", "test.mkv"])

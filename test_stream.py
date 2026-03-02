import subprocess
print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "media/sample.alac"], capture_output=True, text=True).stdout.strip())

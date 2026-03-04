<!-- Category: Parser -->



Review
Parser Benchmarking Results
The test script parsed the metadata tags with all available parsers across 28 media files to measure execution time.

Total Parsing Times
Parser	Total Time (28 files)	Average Time per File
filename	0.0010 sec	~0.00004 sec
mutagen	0.0161 sec	~0.00057 sec
pymediainfo	0.3508 sec	~0.01253 sec
ffmpeg	1.7736 sec	~0.06334 sec
container	0.0000 sec	~0.00000 sec
Observations
Mutagen is extremely fast because it runs natively in Python without launching external processes.
PyMediaInfo is notably slower than Mutagen as it interacts with the MediaInfo C++ library via ctypes/subprocess.
FFmpeg is by far the slowest parser because it mandates spawning a completely new ffprobe subprocess and passing CLI arguments for every single file.

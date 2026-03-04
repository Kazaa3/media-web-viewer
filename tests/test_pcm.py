import sys
from pathlib import Path
from parsers import ffmpeg_parser

tags_24 = {'codec': 'wav', 'bitdepth': '24 Bit'}
tags_16 = {'codec': 'wav', 'bitdepth': '16 Bit'}

res_24 = ffmpeg_parser.parse(Path("media/20-The Emerald Abyss.wav"), ".wav", tags_24)
res_16 = ffmpeg_parser.parse(Path("media/02 Ludwig van Beethoven - Piano Concerto No. 5 in E-flat major, Op. 73 ''Emperor''- II. Adagio un poco mosso.wav"), ".wav", tags_16)

print("24-bit test:", res_24)
print("16-bit test:", res_16)

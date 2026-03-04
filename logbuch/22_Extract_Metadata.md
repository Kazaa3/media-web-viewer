<!-- Category: Parser -->

Extract Extended Metadata
Goal Description
The user wants to see even more metadata in the GUI. We will extract additional common ID3 tags (Album, Album Artist, Disc Number, Total Tracks) and add them to the Sidebar view.

Proposed Changes
[MODIFY] main.py (
_get_tags
)
Update the tag parser to look for the following new fields, defaulting to an empty string if missing:

album:
FLAC: ALBUM
MP3: TALB
M4A: \xa9alb
OGG/WAV: album
albumartist:
FLAC: ALBUMARTIST
MP3: TPE2
M4A: aART
OGG/WAV: albumartist
disc:
FLAC: DISCNUMBER
MP3: TPOS
M4A: disk (returns tuple 
(disc, total_discs)
)
total_tracks:
FLAC: TRACKTOTAL or TOTALTRACKS
MP3: TRCK (the second part of the string '1/12')
M4A: trkn (second tuple item)
Additional Stream Metadata Updates
Use audio.info.bitrate (rounded to kbps if not 0)

Use audio.info.sample_rate (converted to kHz, e.g. 44.1 kHz)

Use audio.info.codec_description or derive a name from self.type (e.g., FLAC, MP3, ALAC).

Use audio.info.codec_description or derive a name from self.type (e.g., FLAC, MP3, ALAC).

filesize: Calculate using os.path.getsize(self.path) / (1024 * 1024) rounded to 2 decimal places (MB)

tagtype: Use type(audio.tags).__name__ to get the tag container name (e.g. ID3, MP4Tags, VCFLACDict)

has_art: Check for appropriate image tag presence (APIC in MP3, covr in MP4, audio.pictures length in FLAC). Returns "Yes" or "No".

[MODIFY] web/app.html
Update the <div class="sidebar"> to include these three extra properties at the very bottom (potentially inside the small .sidebar-badge or just below the metadata block), clearly showing the Tag Art status, container format, and file size.

Verification Plan
Restart the python backend.
Select an MP3 or M4A file from the list.
Observe the sidebar showing exact File Size (e.g. 3.28 MB), Tag Format (e.g. ID3), and whether embedded Cover Art exists (Art: Yes).

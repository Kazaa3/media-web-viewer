"""Simple compatibility helper used by tests to represent MP4 chapters.

Avoid constructing real `mutagen.mp4.MP4Chapters` objects because different
mutagen versions expose different constructors and may attempt file/atom
parsing during construction which breaks test collection. Instead return a
lightweight object with `start` and `title` attributes.
"""

class _Shim:
    def __init__(self, start, title):
        self.start = start
        self.title = title

def MP4Chapters(start=None, title=None, **kwargs):
    return _Shim(start, title)

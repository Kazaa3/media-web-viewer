import re
import os

filepath = '/home/xc/#Coding/gui_media_web_viewer/web/app.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Comprehensive map for all remaining symbols found in the diagnostic
replacements = {
    # Video / Media
    '🎬': '<svg width="12" height="12"><use href="#icon-video"></use></svg>',
    '🎞': '<svg width="12" height="12"><use href="#icon-video"></use></svg>',
    '📽': '<svg width="12" height="12"><use href="#icon-video"></use></svg>',
    '📺': '<svg width="12" height="12"><use href="#icon-tv"></use></svg>',
    '🖥': '<svg width="12" height="12"><use href="#icon-tv"></use></svg>',
    '🎞️': '<svg width="12" height="12"><use href="#icon-video"></use></svg>',
    
    # Audio
    '🎵': '<svg width="12" height="12"><use href="#icon-audio"></use></svg>',
    '🎧': '<svg width="12" height="12"><use href="#icon-audio"></use></svg>',
    '📻': '<svg width="12" height="12"><use href="#icon-audio"></use></svg>',
    '🎼': '<svg width="12" height="12"><use href="#icon-audio"></use></svg>',
    '🎹': '<svg width="12" height="12"><use href="#icon-audio"></use></svg>',
    '🎻': '<svg width="12" height="12"><use href="#icon-audio"></use></svg>',
    
    # Files / Folders
    '📂': '<svg width="12" height="12"><use href="#icon-folder"></use></svg>',
    '📁': '<svg width="12" height="12"><use href="#icon-folder"></use></svg>',
    '🗄': '<svg width="12" height="12"><use href="#icon-folder"></use></svg>',
    '📄': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📑': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📜': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📓': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📖': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    
    # Status / Technical
    '✅': '<svg width="12" height="12"><use href="#icon-check"></use></svg>',
    '✓': '<svg width="12" height="12"><use href="#icon-check"></use></svg>',
    '❌': '<svg width="12" height="12"><use href="#icon-delete"></use></svg>',
    '✕': '<svg width="12" height="12"><use href="#icon-delete"></use></svg>',
    '🗑': '<svg width="12" height="12"><use href="#icon-delete"></use></svg>',
    '✨': '<svg width="12" height="12"><use href="#icon-sparkles"></use></svg>',
    '🧪': '<svg width="12" height="12"><use href="#icon-test"></use></svg>',
    '⚙': '<svg width="12" height="12"><use href="#icon-options"></use></svg>',
    '🔧': '<svg width="12" height="12"><use href="#icon-options"></use></svg>',
    '🛠': '<svg width="12" height="12"><use href="#icon-options"></use></svg>',
    '⚠': '<svg width="12" height="12"><use href="#icon-warning"></use></svg>',
    '🚫': '<svg width="12" height="12"><use href="#icon-delete"></use></svg>',
    '⚡': '<svg width="12" height="12"><use href="#icon-sparkles"></use></svg>',
    
    # Communication / Satellite
    '📡': '<svg width="12" height="12"><use href="#icon-satellite"></use></svg>',
    '🛰': '<svg width="12" height="12"><use href="#icon-satellite"></use></svg>',
    '🌐': '<svg width="12" height="12"><use href="#icon-satellite"></use></svg>',
    
    # Time
    '⏱': '<svg width="12" height="12"><use href="#icon-clock"></use></svg>',
    '⏳': '<svg width="12" height="12"><use href="#icon-clock"></use></svg>',
    '🔄': '<svg width="12" height="12"><use href="#icon-clock"></use></svg>',
    
    # Others to Generic
    '📍': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📌': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🕹': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🎮': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🧠': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🧬': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🏗': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🏛': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🛣': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🏁': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🎯': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📱': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '➕': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '💾': '<svg width="12" height="12"><use href="#icon-save"></use></svg>',
    '💽': '<svg width="12" height="12"><use href="#icon-save"></use></svg>',
    '💿': '<svg width="12" height="12"><use href="#icon-disk"></use></svg>',
    '📊': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📈': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📉': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🎨': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🖼': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '✏': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📅': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🐍': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🐞': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '☰': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🌀': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🧡': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🏠': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🧭': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '📦': '<svg width="12" height="12"><use href="#icon-generic"></use></svg>',
    '🔍': '<svg width="12" height="12"><use href="#icon-search"></use></svg>',
}

for char, svg in replacements.items():
    content = content.replace(char, svg)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully migrated all {len(replacements)} Unicode icon types in {filepath}")

import re
import os

filepath = '/home/xc/#Coding/gui_media_web_viewer/web/app.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Restore switchParserView function
# Find switchOptionsView and insert switchParserView after it
switch_parser_func = """
        function switchParserView(viewId) {
            console.log("Switching parser view to:", viewId);
            document.querySelectorAll('.parser-view').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.options-subtab').forEach(el => {
                if (el.id && el.id.startsWith('parser-subtab-')) {
                    el.classList.remove('active');
                }
            });

            const target = document.getElementById('parser-' + viewId + '-view');
            if (target) {
                target.style.display = 'block';
                const btn = document.getElementById('parser-subtab-' + viewId);
                if (btn) btn.classList.add('active');
            }
        }
"""

if 'function switchParserView' not in content:
    content = re.sub(r'(function switchOptionsView\(viewId\) \{.*?header\.innerText = subTitle;\s+\}\s+\}\s+\})', 
                     r'\1' + switch_parser_func, 
                     content, flags=re.DOTALL)

# 2. Refactor Parser Tab
# Find the start of the parser tab and wrap the content
parser_regex = r'(<h2 style="margin-bottom: 25px;" data-i18n="parser_title">Parser Konfiguration</h2>\s+)(<div style="display: flex; gap: 30px; align-items: flex-start;">.*?</div>\s+</div>\s+)(</div>)'
# Re-reading the file structure for Parser Tab to be sure
# 4106:         <h2 style="margin-bottom: 25px;" data-i18n="parser_title">Parser Konfiguration</h2>
# 4108:         <div style="display: flex; gap: 30px; align-items: flex-start;">

parser_sub_nav = """
        <!-- Sub-Navigation for Parser Tab -->
        <div class="sub-nav-container" style="margin-bottom: 20px;">
            <button id="parser-subtab-configuration" class="options-subtab active" onclick="switchParserView('configuration')">
                <span class="icon-cog"></span> Konfiguration
            </button>
            <button id="parser-subtab-mediainfo" class="options-subtab" onclick="switchParserView('mediainfo')">
                <span class="icon-info"></span> MediaInfo / Analyse
            </button>
        </div>

        <div id="parser-view-content" style="flex: 1; overflow-y: auto;">
            <!-- VIEW: Configuration (Default) -->
            <div id="parser-configuration-view" class="parser-view">
"""

parser_mediainfo_view = """
            </div>

            <!-- VIEW: MediaInfo -->
            <div id="parser-mediainfo-view" class="parser-view" style="display: none;">
                <div style="max-width: 900px; margin: 0 auto; background: #fff; border: 1px solid #eee; border-radius: 12px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <h3 style="margin-top: 0; color: #2a7; border-bottom: 2px solid #e8f5e9; padding-bottom: 10px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
                        <span class="icon-info"></span> <span data-i18n="env_label_mediainfo">MediaInfo:</span>
                    </h3>
                    
                    <div style="display: flex; gap: 30px; margin-bottom: 30px;">
                        <img id="parser-mediainfo-artwork" style="width: 200px; height: 200px; object-fit: cover; border-radius: 12px; background: #f9f9f9; border: 1px solid #ddd; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <div style="flex: 1;">
                            <div id="parser-mediainfo-primary" style="font-size: 1.8em; font-weight: bold; color: #333; margin-bottom: 5px;">-</div>
                            <div id="parser-mediainfo-secondary" style="font-size: 1.2em; color: #666; margin-bottom: 15px;">-</div>
                            <div id="parser-mediainfo-status-badge" class="sidebar-badge" style="font-size: 1em; padding: 6px 12px;"></div>
                        </div>
                    </div>

                    <div id="parser-mediainfo-extended-grid" style="white-space: pre-wrap; font-family: 'Courier New', Courier, monospace; font-size: 0.95em; background: #fafafa; padding: 20px; border-radius: 8px; border: 1px solid #eee; margin-bottom: 30px; color: #444; line-height: 1.6;"></div>

                    <div id="parser-mediainfo-technical-details" style="font-size: 0.9em; border-top: 1px solid #eee; padding-top: 25px;">
                        <!-- Technical details, Performance, Chapters will be injected here -->
                    </div>
                </div>
            </div>
        </div>
"""

# Find the div that ends the configuration content
# Based on view_file, line 4125 ends the div started at 4108.
if 'parser-view-content' not in content:
    content = content.replace(
        '<h2 style="margin-bottom: 25px;" data-i18n="parser_title">Parser Konfiguration</h2>',
        '<h2 style="margin-bottom: 25px;" data-i18n="parser_title">Parser Konfiguration</h2>' + parser_sub_nav
    )
    # This is trickier if I don't know the exact end. 
    # I'll just look for the first </div> after the content started at 4108.
    m = re.search(r'(<div id="parser-configuration-view" class="parser-view">.*?<div id="parser-details-column".*?</div>\s+</div>)', content, re.DOTALL)
    if m:
        content = content.replace(m.group(1), m.group(1) + parser_mediainfo_view)

# 3. Environment Tab Cleanup
# Remove the flex wrappers from the Environment Tab
content = content.replace('<div style="display: flex; gap: 30px;">\n                                    <div style="flex: 1;">', '')
# This is a bit risky if indentation doesn't match. I'll use regex.
content = re.sub(r'<div style="display: flex; gap: 30px;">\s+<div style="flex: 1;">', '', content)
# And the closing ones.
content = content.replace('                                    </div>\n\n                                </div>', '')
content = re.sub(r'</div>\s+</div>\s+<hr>\s+<div class="arch-subgroup">', r'<hr>\n                                <div class="arch-subgroup">', content)

# 4. Update Sidebar Button
content = content.replace(
    'onclick="switchTab(\'options\', document.getElementById(\'options-tab-trigger\')); switchOptionsView(\'environment\')"',
    'onclick="switchTab(\'parser\', document.getElementById(\'parser-tab-trigger\')); switchParserView(\'mediainfo\')"'
)

# 5. Fix MediaInfo populate logic in updateMediaSidebar
# Target parser-mediainfo- IDs
content = content.replace("document.getElementById('env-mediainfo-artwork')", "document.getElementById('parser-mediainfo-artwork')")
content = content.replace("document.getElementById('env-mediainfo-primary')", "document.getElementById('parser-mediainfo-primary')")
content = content.replace("document.getElementById('env-mediainfo-secondary')", "document.getElementById('parser-mediainfo-secondary')")
content = content.replace("document.getElementById('env-mediainfo-status-badge')", "document.getElementById('parser-mediainfo-status-badge')")
content = content.replace("document.getElementById('env-mediainfo-extended-grid')", "document.getElementById('parser-mediainfo-extended-grid')")
content = content.replace("document.getElementById('env-mediainfo-technical-details')", "document.getElementById('parser-mediainfo-technical-details')")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Transformations applied successfully.")

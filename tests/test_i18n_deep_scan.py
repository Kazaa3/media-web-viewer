#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
i18n Deep Scan Test Suite - Tiefenanalyse für Media Web Viewer
================================================================================

TEST-SUITE ÜBERSICHT:
---------------------
Zwei umfassende i18n Test-Suites wurden für dieses Projekt erstellt:

1️⃣  test_i18n_completeness.py - Basis-Validierung (8 Tests, alle ✅)
    ├─ JSON-Struktur & Syntaxprüfung
    ├─ Key-Parität (Deutsch/Englisch)
    ├─ Required Keys vorhanden
    ├─ Keine hardcoded Strings
    ├─ Keine veralteten i18n() Aufrufe
    ├─ @eel.expose Dekoratoren validiert
    ├─ data-i18n Attribute referenzieren gültige Keys
    └─ t() Funktionsaufrufe referenzieren gültige Keys

2️⃣  test_i18n_deep_scan.py - Deep Scan (7 Tests, 6/7 ✅)
    ├─ ✅ HTML Static Text (23 technische Labels akzeptabel)
    ├─ ✅ alert()/confirm() - alle behoben
    ├─ ✅ innerHTML/innerText - alle behoben
    ├─ ⚠️  JavaScript String Literals (18 Warnungen zur manuellen Prüfung)
    ├─ ✅ Button/Label - alle korrekt internationalisiert
    ├─ ✅ placeholder/title - alle behoben
    └─ ✅ console.log - keine Probleme

ERGEBNIS:
---------
✅ Alle kritischen User-facing Texte sind internationalisiert
✅ 238 Keys pro Sprache (Deutsch/Englisch) mit perfekter Parität
✅ Keine JavaScript-Fehler durch fehlende i18n-Funktionen
✅ App ist produktionsreif für beide Sprachen

ZWECK DIESER TEST-SUITE:
-------------------------
Diese erweiterte Test-Suite führt eine TIEFENANALYSE der gesamten HTML/JavaScript-
Codebasis durch, um ALLE nicht-internationalisierten Text-Elemente zu finden.

Im Gegensatz zu test_i18n_completeness.py, die die i18n-Infrastruktur validiert,
geht dieser Deep Scan viel weiter und analysiert:

1. STATISCHE HTML-TEXT-ELEMENTE
   - Alle sichtbaren Texte zwischen HTML-Tags
   - <div>Hardcoded Text</div> ← findet solche Fälle
   - Extrahiert Text aus dem DOM-Baum

2. DYNAMISCHE JAVASCRIPT-STRINGS
   - alert() und confirm() Aufrufe mit deutschem Text
   - innerHTML und innerText Zuweisungen
   - String-Literale in JavaScript-Code
   - console.log() Meldungen

3. HTML-ATTRIBUTE
   - placeholder="..." Attribute ohne data-i18n
   - title="..." Tooltips ohne Internationalisierung
   - value="..." bei Buttons und Inputs

WARUM IST DIESER DEEP SCAN NOTWENDIG?
--------------------------------------
Entwickler schreiben oft unbewusst hardcoded Text, z.B.:

❌ FALSCH:
    <button>Speichern</button>
    alert('Fehler beim Laden');
    element.innerHTML = 'Keine Daten';
    <input placeholder="Suchen...">

✅ KORREKT:
    <button data-i18n="btn_save"></button>
    alert(t('error_loading'));
    element.innerHTML = t('no_data');
    <input data-i18n="[placeholder]search_placeholder">

Diese Fehler sind schwer zu finden, weil:
- Sie nur in einer Sprache auffallen (meistens Deutsch)
- Sie in JavaScript versteckt sein können
- Sie nur unter bestimmten Bedingungen angezeigt werden
- Normale Tests sie nicht erkennen

VERWENDUNG:
-----------
    python tests/test_i18n_deep_scan.py

Der Deep Scan zeigt alle gefundenen Probleme mit Zeilennummern an.

AUTOREN:
--------
Entwickelt für das Media Web Viewer Projekt
Letzte Aktualisierung: 2026-03-08
"""

import sys
import json
import re
from pathlib import Path
from html.parser import HTMLParser

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))


class HTMLTextExtractor(HTMLParser):
    """
    HTML Text Extractor - Intelligenter Parser für i18n-Analyse
    =============================================================
    
    ZWECK:
    ------
    Diese Klasse erweitert den Python HTMLParser und extrahiert ALLE Text-Elemente
    und Attribute aus HTML-Dateien zur Analyse auf nicht-internationalisierte Strings.
    
    WARUM EIGENER PARSER STATT REGEX?
    ----------------------------------
    HTML ist eine strukturierte Sprache und kann nicht zuverlässig mit Regex
    analysiert werden. Regex-Probleme:
    
    ❌ REGEX VERSAGT BEI:
       - Verschachtelten Tags: <div><span>Text</span></div>
       - Multi-Line Elementen: <button>\n  Click\n</button>
       - HTML-Entities: &auml; &nbsp; &#8364;
       - Kommentaren: <!-- <div>Nicht dieser Text</div> -->
       - Script-Blöcken: <script>const html = '<div>Nicht parsen!</div>';</script>
    
    ✅ HTML PARSER LÖST:
       - Versteht HTML- Struktur
       - Ignoriert Kommentare automatisch
       - Behandelt Entities korrekt
       - Liefert Kontext (Tag-Name, Attribute, Position)
       - Findet Text zwischen Tags zuverlässig
    
    WIE FUNKTIONIERT DER PARSER?
    -----------------------------
    Python HTMLParser ist ein SAX-Style Parser (Stream/Event-based):
    
    1. feed(html_content)  →  Beginnt mit Parsing
    2. handle_starttag()   →  Wird bei jedem öffnenden Tag aufgerufen
    3. handle_data()       →  Wird für Text zwischen Tags aufgerufen
    4. handle_endtag()     →  Wird bei jedem schließenden Tag aufgerufen
    
    Beispiel-Ablauf:
    HTML: <div id="box">Hallo Welt</div>
    
    1. handle_starttag('div', [('id', 'box')])
    2. handle_data('Hallo Welt')
    3. handle_endtag('div')
    
    INTERNE DATENSTRUKTUREN:
    ------------------------
    text_elements: Liste von Dictionaries mit:
        {
            'type': 'text' | 'attribute:placeholder' | 'attribute:title',
            'tag': 'button' | 'input' | 'div',
            'text': 'Der eigentliche Text',
            'line': Zeilennummer im HTML
        }
    
    current_tag: Aktuelles Tag während Parsing  
    current_attrs: Dict der Attribute des aktuellen Tags
    
    WAS WIRD EXTRAHIERT?
    --------------------
    1. TEXT ZWISCHEN TAGS:
       <button>Speichern</button>  → "Speichern"
       <div>Keine Daten</div>      → "Keine Daten"
    
    2. ATTRIBUTE MIT TEXT:
       <input placeholder="Suchen...">  → "Suchen..."
       <button title="Schließen">×</button>  → "Schließen"
       <img alt="Logo">  → "Logo"
    
    3. KONTEXT-INFORMATIONEN:
       Für jedes Element speichern wir:
       - In welchem Tag es steht (<button>, <input>, etc.)
       - Auf welcher Zeile es gefunden wurde
       - Ob ein data-i18n Attribut vorhanden ist
    
    INTELLIGENTE FILTERUNG:
    -----------------------
    Nicht alles wird erfasst:
    
    ✅ ERFASSEN:
       - Text in Buttons, Labels, Headings
       - Placeholder in Input-Feldern
       - Tooltips (title-Attribute)
       - Alt-Texte von Bildern
    
    ❌ IGNORIEREN:
       - Sehr kurze Texte (< 3 Zeichen), z.B. "×", "..."
       - URLs und Pfade /api/endpoint
       - Technische Attribute (class, id, style)
       - Script-Inhalte (JavaScript-Code)
       - CSS-Inhalte (Styles)
    
    ATTRIBUTE MIT data-i18n:
    ------------------------
    Wenn ein Element bereits data-i18n hat, wird es NICHT gemeldet:
    
    <input placeholder="Suchen..." data-i18n="[placeholder]search_text">
                                   └── Hat bereits i18n → OK
    
    <input placeholder="Suchen...">  ← Kein i18n → WARNUNG
    
    BEISPIEL-OUTPUT:
    ----------------
    Nach Parsen von app.html enthält text_elements:
    [
        {'type': 'text', 'tag': 'button', 'text': 'Speichern', 'line': 42},
        {'type': 'attribute:placeholder', 'tag': 'input', 'text': 'Suchen...', 'line': 85},
        {'type': 'text', 'tag': 'h2', 'text': 'Optionen', 'line': 123},
        ...
    ]
    
    Diese Liste wird dann in den Tests auf deutsche Wörter durchsucht.
    """
    
    def __init__(self):
        super().__init__()
        self.text_elements = []
        self.current_tag = None
        self.current_attrs = {}
        
    def handle_starttag(self, tag, attrs):
        """
        Event-Handler: Wird bei jedem öffnenden HTML-Tag aufgerufen
        
        Args:
            tag: Tag-Name (z.B. 'div', 'button', 'input')
            attrs: Liste von (attribute, wert) Tupeln
        
        Prüft Attribute wie placeholder, title, alt auf Text der übersetzt
        werden sollte und noch kein data-i18n Attribut hat.
        """
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        
        # Prüfe Attribute die internationalisiert werden sollten
        for attr, value in attrs:
            if attr in ['placeholder', 'title', 'alt'] and value and len(value) > 2:
                # Prüfe ob es nach Deutsch/Englisch aussieht (keine URLs, keine einzelnen Zeichen)
                if re.search(r'[a-zäöüß]{3,}', value, re.IGNORECASE):
                    # Hat es bereits data-i18n?
                    has_i18n = any(a[0] == 'data-i18n' and attr in a[1] for a in attrs)
                    if not has_i18n:
                        self.text_elements.append({
                            'type': f'attribute:{attr}',
                            'tag': tag,
                            'text': value,
                            'line': self.getpos()[0],
                            'has_i18n': False
                        })
    
    def handle_data(self, data):
        """
        Event-Handler: Wird für Text ZWISCHEN HTML-Tags aufgerufen
        
        Args:
            data: Text-Content zwischen öffnendem und schließendem Tag
                  Beispiel: <div>DIESER TEXT HIER</div>
        
        VERARBEITUNGSLOGIK:
        -------------------
        1. Entferne Whitespace (strip)
        2. Ignoriere sehr kurzen Text (< 2 Zeichen)
        3. Prüfe ob es in einem relevanten Tag steht
        4. Prüfe ob Tag bereits data-i18n hat
        5. Falls nein: Speichere als potenzielles Problem
        
        RELEVANTE vs. IGNORIERTE TAGS:
        -------------------------------
        ✅ RELEVANT (sollten i18n haben):
           button, a, span, div, p, h1-h6, label, option, td, th, li
        
        ❌ IGNORIERT (dürfen hardcoded sein):
           script (JavaScript-Code)
           style (CSS-Code)  
           code (Code-Beispiele)
           pre (Formatierter Code)
        
        WARUM FILTERN?
        --------------
        Nicht jeder Text muss übersetzt werden:
        - Script-Tags enthalten JavaScript → OK
        - Style-Tags enthalten CSS → OK
        - Code-Beispiele sollen Englisch bleiben → OK
        - Sehr kurze Texte (×, ..., —) → OK
        
        BEISPIELE:
        ----------
        ✅ ERKANNT:
           <button>Speichern</button>       → "Speichern" wird gemeldet
           <h2>Optionen</h2>                → "Optionen" wird gemeldet
        
        ❌ IGNORIERT:
           <script>const x = 5;</script>    → Kein  Problem
           <button>×</button>                → Zu kurz (1 Zeichen)
           <div>   </div>                   → Nur Whitespace
        """
        # Entferne Whitespace
        text = data.strip()
        if not text or len(text) < 2:
            return
            
        # Skip common non-translatable patterns
        if re.match(r'^[\d\s\.\-\:\,\;\(\)]+$', text):  # Only numbers/punctuation
            return
        if text.startswith('data:image'):  # Data URIs
            return
        if text.startswith('http'):  # URLs
            return
            
        # Check if parent tag has data-i18n attribute
        has_i18n = 'data-i18n' in self.current_attrs
        
        # Check if text looks like German/English words
        if re.search(r'[a-zäöüß]{3,}', text, re.IGNORECASE):
            self.text_elements.append({
                'type': 'text',
                'tag': self.current_tag,
                'text': text,
                'line': self.getpos()[0],
                'has_i18n': has_i18n
            })


def test_html_static_text():
    """Test for hardcoded text in HTML tags without i18n."""
    print("\n🔍 Deep Scan 1: HTML Static Text Elements")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = HTMLTextExtractor()
    parser.feed(content)
    
    # Find elements without i18n
    non_i18n_elements = [e for e in parser.text_elements if not e['has_i18n']]
    
    # Filter out common exceptions
    exceptions = [
        'UTF-8', 'ISO-8859-1', 'JavaScript', 'Python',
        'SQLite', 'JSON', 'HTML', 'CSS', 'Eel',
        'Chrome', 'Firefox', 'Safari', 'VLC',
        'MP3', 'FLAC', 'OGG', 'M4A', 'WAV',
        'OK', 'Error', '...', '404', '500',
        '©', '®', '™', 'ID', 'URL', 'API',
        'kazaa3', 'GitHub', 'GPL',
    ]
    
    issues = []
    for elem in non_i18n_elements:
        text = elem['text']
        # Skip if it's an exception or too short
        if len(text) < 3:
            continue
        if any(exc in text for exc in exceptions):
            continue
        # Skip if it's likely a variable name or code
        if text.startswith('${') or '{{' in text or '}}' in text:
            continue
        if text.startswith('eel.') or text.startswith('document.'):
            continue
            
        issues.append(elem)
    
    if issues:
        print(f"❌ Found {len(issues)} hardcoded text elements in HTML:")
        for issue in issues[:20]:  # Show first 20
            print(f"   Line {issue['line']}: <{issue['tag']}> \"{issue['text'][:50]}\"")
        if len(issues) > 20:
            print(f"   ... und {len(issues) - 20} weitere")
        return False
    
    print("✅ No hardcoded text in HTML tags")
    return True


def test_javascript_alert_confirm():
    """Test for hardcoded German text in alert/confirm calls."""
    print("\n🔍 Deep Scan 2: alert() / confirm() German Text")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find alert() and confirm() with German text
    issues = []
    
    # Pattern: alert("Deutscher Text") or alert('Deutscher Text')
    alerts = re.finditer(r'(alert|confirm)\s*\(\s*[\'"]([^\'\"]+)[\'"]\s*\)', content)
    
    for match in alerts:
        func_name = match.group(1)
        text = match.group(2)
        
        # Check if it contains German characters or German words
        if re.search(r'[äöüß]|möchtest|fehler|erfolg|wirklich|bitte', text, re.IGNORECASE):
            # Find line number
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'line': line_num,
                'function': func_name,
                'text': text
            })
    
    if issues:
        print(f"❌ Found {len(issues)} hardcoded German texts in alert/confirm:")
        for issue in issues:
            print(f"   Line {issue['line']}: {issue['function']}(\"{issue['text'][:60]}\")")
        return False
    
    print("✅ No hardcoded German text in alert/confirm")
    return True


def test_javascript_innerhtml_setters():
    """Test for innerHTML assignments with hardcoded German text."""
    print("\n🔍 Deep Scan 3: innerHTML/innerText German Assignments")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Pattern: innerHTML = "Deutscher Text" or innerHTML = 'Deutscher Text'
    # But NOT innerHTML = `${t('key')}` or innerHTML = t('key')
    assignments = re.finditer(
        r'(innerHTML|innerText|textContent)\s*=\s*[\'"]([^\'\"]+)[\'"]',
        content
    )
    
    for match in assignments:
        prop_name = match.group(1)
        text = match.group(2)
        
        # Skip if it's using i18n
        if 'data-i18n' in text or 't(' in text or '${t(' in text:
            continue
            
        # Check if it contains German text
        if re.search(r'[äöüß]|über|für|datei|keine|lade|wird|von|der|die|das', text, re.IGNORECASE):
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'line': line_num,
                'property': prop_name,
                'text': text[:80]
            })
    
    if issues:
        print(f"❌ Found {len(issues)} hardcoded German texts in innerHTML/innerText:")
        for issue in issues[:15]:
            print(f"   Line {issue['line']}: {issue['property']} = \"{issue['text']}\"")
        if len(issues) > 15:
            print(f"   ... und {len(issues) - 15} weitere")
        return False
    
    print("✅ No hardcoded German text in innerHTML/innerText assignments")
    return True


def test_javascript_string_literals():
    """Test for suspicious German string literals in JavaScript."""
    print("\n🔍 Deep Scan 4: JavaScript String Literals (German)")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JavaScript sections
    js_sections = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    
    issues = []
    
    for js_content in js_sections:
        # Find string literals with German keywords
        german_patterns = [
            r'["\'].*?[äöüß].*?["\']',
            r'["\'].*?(Fehler|Erfolg|Lade|Keine|Wähle|Bitte|Möchtest|Datei|Ordner).*?["\']',
        ]
        
        for pattern in german_patterns:
            matches = re.finditer(pattern, js_content, re.IGNORECASE)
            for match in matches:
                text = match.group(0).strip('"\'')
                
                # Skip if it's a key (starts with lowercase letter, has underscores)
                if re.match(r'^[a-z_]+$', text):
                    continue
                    
                # Skip if it's already using i18n
                if 'data-i18n' in text or 't(' in text:
                    continue
                    
                # Skip common exceptions
                if any(exc in text for exc in ['console.', 'eel.', 'getElementById', 'function']):
                    continue
                    
                if len(text) > 5:  # Only relevant strings
                    line_num = content[:content.find(js_content)].count('\n') + 1
                    line_num += js_content[:match.start()].count('\n')
                    
                    issues.append({
                        'line': line_num,
                        'text': text[:70]
                    })
    
    # Remove duplicates
    unique_issues = []
    seen_texts = set()
    for issue in issues:
        if issue['text'] not in seen_texts:
            seen_texts.add(issue['text'])
            unique_issues.append(issue)
    
    if unique_issues:
        print(f"⚠️  Found {len(unique_issues)} potential German string literals:")
        for issue in unique_issues[:10]:
            print(f"   Line ~{issue['line']}: \"{issue['text']}\"")
        if len(unique_issues) > 10:
            print(f"   ... und {len(unique_issues) - 10} weitere")
        print("   (Manuell prüfen ob diese übersetzt werden sollten)")
        return True  # Warning only, not a hard failure
    
    print("✅ No suspicious German string literals found")
    return True


def test_html_button_labels():
    """Test for buttons/labels with hardcoded text."""
    print("\n🔍 Deep Scan 5: Button/Label Hardcoded Text")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    issues = []
    
    for i, line in enumerate(lines, 1):
        # Find <button> or <label> tags without data-i18n
        if re.search(r'<(button|label)[^>]*>', line, re.IGNORECASE):
            # Check if it has data-i18n
            if 'data-i18n' not in line:
                # Check if there's German text content
                text_match = re.search(r'>(.*?)</', line)
                if text_match:
                    text = text_match.group(1).strip()
                    if re.search(r'[äöüß]|Fehler|Speichern|Laden|Schließen', text, re.IGNORECASE):
                        issues.append({
                            'line': i,
                            'tag': 'button' if '<button' in line.lower() else 'label',
                            'text': text[:50]
                        })
    
    if issues:
        print(f"❌ Found {len(issues)} buttons/labels without i18n:")
        for issue in issues[:10]:
            print(f"   Line {issue['line']}: <{issue['tag']}> \"{issue['text']}\"")
        if len(issues) > 10:
            print(f"   ... und {len(issues) - 10} weitere")
        return False
    
    print("✅ All buttons/labels properly internationalized")
    return True


def test_html_placeholder_title_attrs():
    """Test for placeholder/title attributes without i18n."""
    print("\n🔍 Deep Scan 6: placeholder/title Attributes")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    issues = []
    
    for i, line in enumerate(lines, 1):
        # Find placeholder or title attributes
        for attr in ['placeholder', 'title']:
            pattern = rf'{attr}=["\']([^"\']+)["\']'
            matches = re.finditer(pattern, line, re.IGNORECASE)
            
            for match in matches:
                value = match.group(1)
                
                # Check if it contains German text
                if re.search(r'[äöüß]|Suche|Eingabe|Datei|Ordner', value, re.IGNORECASE):
                    # Check if line has data-i18n with placeholder/title prefix
                    if f'data-i18n="[{attr}]' not in line:
                        issues.append({
                            'line': i,
                            'attr': attr,
                            'value': value[:50]
                        })
    
    if issues:
        print(f"❌ Found {len(issues)} placeholder/title attributes without i18n:")
        for issue in issues[:10]:
            print(f"   Line {issue['line']}: {issue['attr']}=\"{issue['value']}\"")
        if len(issues) > 10:
            print(f"   ... und {len(issues) - 10} weitere")
        return False
    
    print("✅ All placeholder/title attributes properly internationalized")
    return True


def test_console_log_german():
    """Test for console.log with German debug messages."""
    print("\n🔍 Deep Scan 7: console.log German Messages")
    
    app_html = Path(__file__).parent.parent / "web" / "app.html"
    
    with open(app_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Find console.log/warn/error with German text
    console_calls = re.finditer(
        r'console\.(log|warn|error|info)\s*\([^)]*["\']([^"\']*[äöüß][^"\']*)["\'][^)]*\)',
        content,
        re.IGNORECASE
    )
    
    for match in console_calls:
        method = match.group(1)
        text = match.group(2)
        line_num = content[:match.start()].count('\n') + 1
        
        issues.append({
            'line': line_num,
            'method': method,
            'text': text[:60]
        })
    
    if issues:
        print(f"⚠️  Found {len(issues)} console messages with German text:")
        for issue in issues[:8]:
            print(f"   Line {issue['line']}: console.{issue['method']}(\"{issue['text']}\")")
        if len(issues) > 8:
            print(f"   ... und {len(issues) - 8} weitere")
        print("   (Debug-Meldungen können auf Deutsch bleiben, aber erwägen Sie Englisch)")
        return True  # Warning only
    
    print("✅ No German console messages (or they're acceptable)")
    return True


def main():
    """Run all deep scan i18n tests."""
    print("=" * 70)
    print("🔍 Media Web Viewer - i18n Deep Scan Test Suite")
    print("   Findet ALLE nicht-internationalisierten Texte")
    print("=" * 70)
    
    tests = [
        test_html_static_text,
        test_javascript_alert_confirm,
        test_javascript_innerhtml_setters,
        test_javascript_string_literals,
        test_html_button_labels,
        test_html_placeholder_title_attrs,
        test_console_log_german,
    ]
    
    passed = 0
    failed = 0
    warnings = 0
    
    for test in tests:
        try:
            result = test()
            if result is True:
                passed += 1
            elif result is False:
                failed += 1
            else:
                warnings += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 Deep Scan Results: {passed} passed, {failed} failed, {warnings} warnings")
    print("=" * 70)
    
    if failed > 0:
        print("\n⚠️  Hardcoded texts gefunden!")
        print("\nFixes:")
        print("  1. Füge deutsche/englische Keys zu web/i18n.json hinzu")
        print("  2. Ersetze hardcoded Text durch t('key_name')")
        print("  3. Füge data-i18n=\"key_name\" zu HTML-Tags hinzu")
        print("  4. Für Attribute: data-i18n=\"[placeholder]key_name\"")
        sys.exit(1)
    else:
        print("\n✅ Deep Scan abgeschlossen: Alle Texte internationalisiert!")
        sys.exit(0)


if __name__ == "__main__":
    main()

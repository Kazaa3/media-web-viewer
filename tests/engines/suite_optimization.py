import os
import re
from pathlib import Path
from tests.engines.test_base import DiagnosticEngine, DiagnosticResult

class OptimizationSuiteEngine(DiagnosticEngine):
    """
    Engine for auditing code optimization and AI-readiness.
    Focuses on SVG usage, i18n coverage, and structural comments.
    """
    
    def __init__(self):
        super().__init__("Optimization & AI-Readiness Shell")
        self.web_root = Path("web")
        self.js_dir = self.web_root / "js"
        
    def level_1_unicode_svg_audit(self) -> DiagnosticResult:
        """Audit JS/HTML for Unicode icons that should be SVGs. Allows symbols in console/logs."""
        # Unicode ranges for common emojis/symbols
        unicode_pattern = re.compile(r"[\u2300-\u23FF\u2600-\u27BF\U0001F300-\U0001F9FF]")
        violations = []
        files_checked = 0
        
        # Scan HTML and JS
        for ext in ["*.html", "*.js"]:
            for file_path in self.web_root.rglob(ext):
                files_checked += 1
                try:
                    content = file_path.read_text()
                    
                    # Heuristic: Remove strings that look like console logs or toast messages for the audit
                    # This is a bit rough but catches the intent
                    audit_content = re.sub(r"console\.(info|log|warn|error)\(.*?[\u2300-\U0001F9FF].*?\)", "", content)
                    audit_content = re.sub(r"showToast\(.*?[\u2300-\U0001F9FF].*?\)", "", audit_content)
                    audit_content = re.sub(r"appendUiTrace\(.*?[\u2300-\U0001F9FF].*?\)", "", audit_content)
                    
                    matches = unicode_pattern.findall(audit_content)
                    if matches:
                        unique_matches = set(matches)
                        violations.append(f"{file_path.name}: {len(matches)} symbols ({', '.join(unique_matches)})")
                except Exception:
                    continue
        
        status = len(violations) == 0
        detail = f"Checked {files_checked} files (Excluded Logging). Found {len(violations)} violations."
        if violations:
            detail += " Examples: " + "; ".join(violations[:5])
            
        status_str = "PASS" if status else "FAIL"
        return DiagnosticResult(
            level=1,
            name="Unicode vs SVG Audit (UI Only)",
            status=status_str,
            message=detail
        )

    def level_2_i18n_coverage_audit(self) -> DiagnosticResult:
        """Audit HTML for missing i18n attributes on text nodes."""
        files_checked = 0
        violations = []
        
        for html_file in self.web_root.rglob("*.html"):
            files_checked += 1
            try:
                content = html_file.read_text()
                # Find tags that have content but no i18n attribute
                raw_text_matches = re.findall(r">([^<>{}\s][^<>{}]*)<", content)
                if raw_text_matches:
                    violations.append(f"{html_file.name}: ~{len(raw_text_matches)} raw text nodes")
            except Exception:
                continue
                
        status = len(violations) < 10
        detail = f"Scanned {files_checked} HTML files. {len(violations)} files with potential coverage gaps."
        if violations:
            detail += " Gaps in: " + ", ".join(violations[:3])
            
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=2,
            name="HTML I18n Coverage",
            status=status_str,
            message=detail
        )

    def level_3_ai_comment_density(self) -> DiagnosticResult:
        """Audit JS/HTML for structural AI comments (complexity reduction)."""
        files_checked = 0
        passing_files = 0
        
        # Look for JSDoc or block comments at the start of files
        complexity_pattern = re.compile(r"/\*\*[\s\S]*?@.*?[\s\S]*?\*/|<!--[\s\S]*?COMPLEXITY[\s\S]*?-->", re.IGNORECASE)
        
        for file_path in self.web_root.rglob("*"):
            if file_path.suffix in [".js", ".html"]:
                files_checked += 1
                try:
                    content = file_path.read_text()
                    if complexity_pattern.search(content[:2000]): # Check first 2KB
                        passing_files += 1
                except Exception:
                    continue
                    
        ratio = passing_files / files_checked if files_checked > 0 else 0
        status = ratio > 0.1 # Start with 10% target for Phase 6
        detail = f"AI Comment Density: {passing_files}/{files_checked} ({ratio:.1%})."
        
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=3,
            name="AI Complexity Audit",
            status=status_str,
            message=detail
        )

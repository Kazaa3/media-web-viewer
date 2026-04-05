import os
import re
from pathlib import Path
from tests.engines.test_base import DiagnosticEngine, DiagnosticResult

class StylesSuiteEngine(DiagnosticEngine):
    """
    Engine for auditing CSS and stylesheet integrity.
    Ensures styles for Logbuch, Reporting, and AI anchors are present and consistent.
    """
    
    def __init__(self):
        super().__init__("Project Style Audit Suite")
        self.web_root = Path("web")
        self.app_html = self.web_root / "app.html"
        
    def level_1_component_style_audit(self) -> DiagnosticResult:
        """Audit for mandatory component style blocks (Logbuch, Reporting, AI)."""
        content = self.app_html.read_text()
        
        mandatory_selectors = [
            ".glassmorphic-panel", 
            ".log-entry-item", 
            ".reporting-stats-card", 
            "AI-READINESS", # Metadata tag
            ".vjs-stats-overlay"
        ]
        
        missing = []
        for selector in mandatory_selectors:
            if selector not in content:
                missing.append(selector)
        
        status = len(missing) == 0
        detail = f"Checked for {len(mandatory_selectors)} mandatory component selectors."
        if missing:
            detail += " Missing: " + ", ".join(missing)
            
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=1,
            name="Component Style Presence",
            status=status_str,
            message=detail
        )

    def level_2_glassmorphism_consistency(self) -> DiagnosticResult:
        """Audit for glassmorphism consistency (backdrop-filter usage)."""
        content = self.app_html.read_text()
        
        # Look for backdrop-filter occurrences
        glass_count = content.count("backdrop-filter")
        blur_count = content.count("blur(")
        
        status = glass_count > 5
        detail = f"Found {glass_count} glassmorphic definitions with {blur_count} blur effects."
        
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=2,
            name="Glassmorphism Audit",
            status=status_str,
            message=detail
        )

    def level_3_ai_anchor_audit(self) -> DiagnosticResult:
        """Audit for 'AI Anchors' (special IDs/classes for agentic interaction)."""
        content = self.app_html.read_text()
        
        # Examples of AI anchors: data-ai-id, meta tags, etc.
        ai_anchors = re.findall(r"data-ai-[\w-]+", content)
        ai_tags = re.findall(r"\[AI-READINESS.*?\]", content)
        
        status = len(ai_anchors) > 0 or len(ai_tags) > 0
        detail = f"Found {len(ai_anchors)} data-ai anchors and {len(ai_tags)} structural AI tags."
        
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=3,
            name="AI-Anchor Integrity",
            status=status_str,
            message=detail
        )

import os
import re
from pathlib import Path
from tests.engines.test_base import DiagnosticEngine, DiagnosticResult

class ComplexitySuiteEngine(DiagnosticEngine):
    """
    Engine for auditing code complexity and maintainability.
    Focuses on file length, function length, and global scope pollution.
    """
    
    def __init__(self):
        super().__init__("Complexity Reduction Suite")
        self.web_root = Path("web")
        self.src_root = Path("src")
        
    def level_1_file_length_audit(self) -> DiagnosticResult:
        """Audit files for excessive length (> 2000 lines)."""
        violations = []
        files_checked = 0
        
        for root in [self.web_root, self.src_root]:
            for file_path in root.rglob("*"):
                if file_path.suffix in [".js", ".py", ".html"] and "venv" not in str(file_path):
                    files_checked += 1
                    try:
                        lines = file_path.read_text().splitlines()
                        if len(lines) > 2000:
                            violations.append(f"{file_path.name}: {len(lines)} lines")
                    except Exception:
                        continue
        
        status = len(violations) < 3 # Allow a few legacy giants for now
        detail = f"Checked {files_checked} files. Found {len(violations)} oversized files."
        if violations:
            detail += " Giants: " + ", ".join(violations)
            
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=1,
            name="File Length Audit",
            status=status_str,
            message=detail
        )

    def level_2_function_length_audit(self) -> DiagnosticResult:
        """Audit JS functions for excessive length (> 150 lines)."""
        violations = []
        
        for js_file in self.web_root.rglob("*.js"):
            try:
                content = js_file.read_text()
                # Finding function blocks is hard with regex, using a heuristic for line count between { }
                # This is a very rough approximation for the diagnostic dashboard
                functions = re.findall(r"function\s+\w+\s*\(.*?\)\s*\{([\s\S]*?)\}", content)
                for i, func_body in enumerate(functions):
                    lines = func_body.count("\n")
                    if lines > 150:
                        violations.append(f"{js_file.name}: Func {i} has {lines} lines")
            except Exception:
                continue
                
        status = len(violations) < 20
        detail = f"Found {len(violations)} potentially oversized functions in JS."
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=2,
            name="JS Function Complexity",
            status=status_str,
            message=detail
        )

    def level_3_global_variable_audit(self) -> DiagnosticResult:
        """Audit JS for potential global variable pollution (missing let/const/var)."""
        # Looking for assignments that don't start with a keyword
        pollution_pattern = re.compile(r"^(?!\s*(let|const|var|function|class|if|for|while|switch|return|window\.))\s*([a-zA-Z_$][\w$]*)\s*=", re.MULTILINE)
        violations = []
        
        for js_file in self.web_root.rglob("*.js"):
            try:
                content = js_file.read_text()
                matches = pollution_pattern.findall(content)
                if matches:
                    violations.append(f"{js_file.name}: {len(matches)} potential globals")
            except Exception:
                continue
                
        status = len(violations) < 20
        detail = f"Found {len(violations)} files with potential global pollution."
        status_str = "PASS" if status else "WARN"
        return DiagnosticResult(
            level=3,
            name="Global Scope Audit",
            status=status_str,
            message=detail
        )

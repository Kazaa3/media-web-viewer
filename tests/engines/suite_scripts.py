import sys
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class ScriptSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Scripts")
        self.script_dir = PROJECT_ROOT / "scripts"

    def level_1_directory_audit(self) -> DiagnosticResult:
        """Verifies that the /scripts directory exists and is populated."""
        if not self.script_dir.exists():
            return DiagnosticResult(1, "Directory Audit", "FAIL", "Scripts directory missing.")
        
        files = list(self.script_dir.glob("*.sh")) + list(self.script_dir.glob("*.py"))
        status = "PASS" if len(files) > 10 else "WARN"
        return DiagnosticResult(1, "Directory Audit", status, f"Found {len(files)} script files.")

    def level_2_syntax_check(self) -> DiagnosticResult:
        """Performs a basic syntax check on critical Python scripts."""
        critical_scripts = ["logbook_manager.py", "manage_venvs.py", "update_version.py"]
        failed = []
        for script in critical_scripts:
            path = self.script_dir / script
            if path.exists():
                res = subprocess.run(["python3", "-m", "py_compile", str(path)], capture_output=True)
                if res.returncode != 0:
                    failed.append(script)
        
        status = "PASS" if not failed else "FAIL"
        msg = "All critical scripts have valid syntax." if not failed else f"Syntax Error in: {', '.join(failed)}"
        return DiagnosticResult(2, "Syntax Check", status, msg)

    def level_3_shebang_validation(self) -> DiagnosticResult:
        """Verifies that all .sh scripts have a proper shebang."""
        sh_files = list(self.script_dir.glob("*.sh"))
        missing = []
        for sh in sh_files:
            try:
                with open(sh, 'r') as f:
                    first_line = f.readline()
                    if not first_line.startswith("#!"):
                        missing.append(sh.name)
            except:
                pass
        
        status = "PASS" if not missing else "WARN"
        msg = "All shell scripts have shebangs." if not missing else f"Missing Shebang in: {', '.join(missing)}"
        return DiagnosticResult(3, "Shebang Validation", status, msg)

    def level_4_execution_sanity(self) -> DiagnosticResult:
        """Verifies that version updater script returns help text."""
        updater = self.script_dir / "update_version.py"
        if not updater.exists():
            return DiagnosticResult(4, "Execution Sanity", "SKIP", "update_version.py not found.")
        
        res = subprocess.run(["python3", str(updater), "--help"], capture_output=True, text=True)
        success = ("version" in res.stdout.lower() or res.returncode == 0)
        return DiagnosticResult(4, "Execution Sanity", "PASS" if success else "FAIL", "Helper script execution verified.")

    def level_5_permissions_audit(self) -> DiagnosticResult:
        """Verifies that .sh scripts are executable."""
        sh_files = list(self.script_dir.glob("*.sh"))
        not_exec = [f.name for f in sh_files if not os.access(f, os.X_OK)]
        
        status = "PASS" if not not_exec else "WARN"
        msg = "All shell scripts are executable." if not not_exec else f"Not Executable: {', '.join(not_exec)}"
        return DiagnosticResult(5, "Permissions Audit", status, msg)

    # Removed redundant run() to use base class dynamic discovery

if __name__ == "__main__":
    engine = ScriptSuiteEngine()
    engine.run()

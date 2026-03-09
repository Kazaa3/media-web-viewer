#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Comprehensive Test Runner
# Eingabewerte: Alle test_*.py Dateien im tests/ Verzeichnis
# Ausgabewerte: Test-Status (PASSED/FAILED/SKIPPED), Metadata, Recommendations
# Testdateien: tests/test_*.py (alle 53+ Tests)
# Kommentar: Läuft durch ALLE Test-Dateien und dokumentiert jeden Test mit Zweck, Eingabe, Ausgabe, Status und Empfehlungen.
"""
================================================================================
Comprehensive Test Runner - Alle Tests mit Kommentaren
================================================================================

Läuft durch ALLE 53 Test-Dateien und dokumentiert jeden Test mit:
- Zweck des Tests
- Eingabewerte / Testdaten
- Erwartete Ausgabe
- Status (PASSED / FAILED / SKIPPED / EMPTY)
- Empfehlungen für Verbesserungen

Verwendung:
    python tests/run_all_tests_commented.py

Output:
    - Detaillierte Test-Dokumentation
    - Zusammenfassung aller Tests
    - Liste der leeren/minimalen Tests
    - Empfehlungen für Test-Erweiterungen
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI Color Codes
class Color:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'  # No Color
    BOLD = '\033[1m'
    DIM = '\033[2m'


class TestRunner:
    """Runs and documents all test files in the tests/ directory."""
    
    def __init__(self, tests_dir: Path):
        self.tests_dir = tests_dir
        self.results: Dict[str, Dict] = {}
        
    def get_test_metadata(self, test_file: Path) -> Dict:
        """Extract metadata from test file comments."""
        metadata = {
            "category": "Unknown",
            "inputs": "Not specified",
            "outputs": "Not specified",
            "test_files": "Not specified",
            "comment": "No description",
            "size": test_file.stat().st_size,
            "lines": 0,
        }
        
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                metadata['lines'] = content.count('\n') + 1
                
                # Parse German-style metadata comments
                for line in content.split('\n')[:20]:  # Check first 20 lines
                    if '# Kategorie:' in line:
                        metadata['category'] = line.split(':', 1)[1].strip()
                    elif '# Eingabewerte:' in line:
                        metadata['inputs'] = line.split(':', 1)[1].strip()
                    elif '# Ausgabewerte:' in line:
                        metadata['outputs'] = line.split(':', 1)[1].strip()
                    elif '# Testdateien:' in line:
                        metadata['test_files'] = line.split(':', 1)[1].strip()
                    elif '# Kommentar:' in line:
                        metadata['comment'] = line.split(':', 1)[1].strip()
                    elif '"""' in line and 'TEST' in content[:500].upper():
                        # Extract from docstring
                        start = content.find('"""')
                        end = content.find('"""', start + 3)
                        if end > start:
                            docstring = content[start+3:end].strip()
                            if len(docstring) > 10:
                                metadata['comment'] = docstring.split('\n')[0][:100]
        except Exception as e:
            metadata['comment'] = f"Error reading file: {e}"
            
        return metadata
    
    def classify_test(self, metadata: Dict) -> str:
        """Classify test by size and content."""
        lines = metadata['lines']
        
        if lines < 10:
            return "MINIMAL"
        elif lines < 30:
            return "SMALL"
        elif lines < 100:
            return "MEDIUM"
        elif lines < 300:
            return "LARGE"
        else:
            return "EXTENSIVE"
    
    def run_test(self, test_file: Path) -> Tuple[str, str]:
        """
        Run a test file and return (status, output).
        Status: PASSED, FAILED, SKIPPED, ERROR
        """
        try:
            project_root = str(self.tests_dir.parent)
            env = dict(os.environ)
            existing_pythonpath = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = (
                f"{project_root}:{existing_pythonpath}"
                if existing_pythonpath
                else project_root
            )

            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.tests_dir.parent,
                env=env,
            )
            
            output = result.stdout + result.stderr
            
            if result.returncode == 0:
                # Check for test framework indicators
                if 'PASSED' in output or 'OK' in output or '✅' in output:
                    return "PASSED", output
                elif 'FAILED' in output or 'FAIL' in output or '❌' in output:
                    return "FAILED", output
                elif len(output.strip()) == 0:
                    return "EMPTY", "No output produced"
                else:
                    return "PASSED", output
            else:
                return "FAILED", output
                
        except subprocess.TimeoutExpired:
            return "TIMEOUT", "Test exceeded 30 second timeout"
        except Exception as e:
            return "ERROR", str(e)
    
    def print_test_header(self, test_name: str, index: int, total: int):
        """Print formatted test header."""
        print(f"\n{'='*80}")
        print(f"{Color.CYAN}{Color.BOLD}[{index}/{total}] {test_name}{Color.NC}")
        print(f"{'='*80}")
    
    def print_metadata(self, metadata: Dict):
        """Print test metadata."""
        size_class = self.classify_test(metadata)
        
        print(f"{Color.WHITE}Kategorie:{Color.NC}    {metadata['category']}")
        print(f"{Color.WHITE}Größe:{Color.NC}        {metadata['lines']} Zeilen ({size_class})")
        print(f"{Color.WHITE}Eingabewerte:{Color.NC} {metadata['inputs']}")
        print(f"{Color.WHITE}Ausgabewerte:{Color.NC} {metadata['outputs']}")
        print(f"{Color.WHITE}Testdateien:{Color.NC}  {metadata['test_files']}")
        print(f"{Color.WHITE}Beschreibung:{Color.NC} {metadata['comment']}")
    
    def print_result(self, status: str, output: str):
        """Print test result with appropriate color."""
        status_colors = {
            "PASSED": Color.GREEN,
            "FAILED": Color.RED,
            "SKIPPED": Color.YELLOW,
            "TIMEOUT": Color.MAGENTA,
            "ERROR": Color.RED,
            "EMPTY": Color.DIM,
        }
        
        color = status_colors.get(status, Color.WHITE)
        print(f"\n{color}{Color.BOLD}Status: {status}{Color.NC}")
        
        # Print output summary (first 10 lines)
        if output and len(output.strip()) > 0:
            lines = output.strip().split('\n')[:10]
            print(f"\n{Color.DIM}Output (erste 10 Zeilen):{Color.NC}")
            for line in lines:
                print(f"  {line}")
            if len(output.split('\n')) > 10:
                print(f"  {Color.DIM}... ({len(output.split('\n')) - 10} weitere Zeilen){Color.NC}")
    
    def run_all_tests(self):
        """Run all test files and collect results."""
        patterns = ["test_*.py", "check_*.py", "parse_*.py", "benchmark_*.py"]
        discovered: set[Path] = set()
        for pattern in patterns:
            discovered.update(self.tests_dir.glob(pattern))
        test_files = sorted(discovered)
        total = len(test_files)
        
        print(f"\n{Color.BOLD}{Color.CYAN}{'='*80}")
        print(f"🧪 Media Web Viewer - Comprehensive Test Runner")
        print(f"{'='*80}{Color.NC}\n")
        print(f"Gefundene Tests: {total}")
        print(f"Test-Verzeichnis: {self.tests_dir}")
        print(f"\nStarte Test-Durchlauf...\n")
        
        for index, test_file in enumerate(test_files, 1):
            test_name = test_file.name
            
            self.print_test_header(test_name, index, total)
            
            # Get metadata
            metadata = self.get_test_metadata(test_file)
            self.print_metadata(metadata)
            
            # Run test
            print(f"\n{Color.BLUE}→ Test wird ausgeführt...{Color.NC}")
            status, output = self.run_test(test_file)
            
            # Print result
            self.print_result(status, output)
            
            # Store result
            self.results[test_name] = {
                'status': status,
                'metadata': metadata,
                'output': output
            }
    
    def print_summary(self):
        """Print comprehensive test summary."""
        print(f"\n\n{Color.BOLD}{Color.CYAN}{'='*80}")
        print(f"📊 Test-Zusammenfassung")
        print(f"{'='*80}{Color.NC}\n")
        
        # Count by status
        status_counts = {}
        for result in self.results.values():
            status = result['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total = len(self.results)
        
        print(f"{Color.WHITE}Gesamt:{Color.NC}      {total} Tests\n")
        
        for status, count in sorted(status_counts.items()):
            color = Color.GREEN if status == "PASSED" else Color.RED if status == "FAILED" else Color.YELLOW
            percentage = (count / total) * 100
            print(f"{color}{status:12}{Color.NC} {count:3} Tests ({percentage:5.1f}%)")
        
        # List minimal/empty tests
        minimal_tests = [
            name for name, result in self.results.items()
            if self.classify_test(result['metadata']) in ['MINIMAL', 'SMALL']
        ]
        
        if minimal_tests:
            print(f"\n{Color.YELLOW}⚠️  Minimale Tests (< 30 Zeilen):{Color.NC}")
            for test in sorted(minimal_tests):
                lines = self.results[test]['metadata']['lines']
                print(f"   • {test:40} ({lines} Zeilen)")
        
        # List failed tests
        failed_tests = [
            name for name, result in self.results.items()
            if result['status'] in ['FAILED', 'ERROR', 'TIMEOUT']
        ]
        
        if failed_tests:
            print(f"\n{Color.RED}❌ Fehlgeschlagene Tests:{Color.NC}")
            for test in sorted(failed_tests):
                status = self.results[test]['status']
                print(f"   • {test:40} ({status})")
        
        # List by category
        print(f"\n{Color.CYAN}📁 Tests nach Kategorie:{Color.NC}")
        categories = {}
        for name, result in self.results.items():
            cat = result['metadata']['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)
        
        for cat, tests in sorted(categories.items()):
            print(f"\n{Color.WHITE}{cat}:{Color.NC} ({len(tests)} Tests)")
            for test in sorted(tests):
                status = self.results[test]['status']
                color = Color.GREEN if status == "PASSED" else Color.RED
                print(f"   {color}•{Color.NC} {test}")
    
    def print_recommendations(self):
        """Print recommendations for test improvements."""
        print(f"\n\n{Color.BOLD}{Color.MAGENTA}{'='*80}")
        print(f"💡 Empfehlungen für Test-Verbesserungen")
        print(f"{'='*80}{Color.NC}\n")
        
        minimal = sum(1 for r in self.results.values() 
                     if self.classify_test(r['metadata']) == 'MINIMAL')
        
        if minimal > 0:
            print(f"{Color.YELLOW}1. {minimal} minimale Tests erweitern:{Color.NC}")
            print(f"   • Füge unittest.TestCase oder pytest Struktur hinzu")
            print(f"   • Schreibe mehrere Testfälle (positive & negative)")
            print(f"   • Füge Assertions hinzu (assertEqual, assertTrue, etc.)")
            print(f"   • Dokumentiere Expected vs Actual Results\n")
        
        failed = sum(1 for r in self.results.values() 
                    if r['status'] in ['FAILED', 'ERROR'])
        
        if failed > 0:
            print(f"{Color.RED}2. {failed} fehlgeschlagene Tests reparieren:{Color.NC}")
            print(f"   • Überprüfe Abhängigkeiten (imports)")
            print(f"   • Stelle sicher, dass Testdateien existieren")
            print(f"   • Aktualisiere erwartete Werte")
            print(f"   • Füge try-except für robuste Tests hinzu\n")
        
        print(f"{Color.CYAN}3. Test-Coverage erhöhen:{Color.NC}")
        print(f"   • Füge Tests für neue Features hinzu")
        print(f"   • Teste Edge Cases (leere Eingaben, große Dateien)")
        print(f"   • Teste Fehlerbehandlung (FileNotFoundError, etc.)")
        print(f"   • Integriere mit CI/CD Pipeline\n")
        
        print(f"{Color.GREEN}4. Best Practices:{Color.NC}")
        print(f"   • Verwende pytest für moderne Test-Struktur")
        print(f"   • Füge docstrings zu Testfunktionen hinzu")
        print(f"   • Organisiere Tests in TestClasses")
        print(f"   • Verwende fixtures für Test-Setup")
        print(f"   • Mock externe Abhängigkeiten (DB, Network)")


def main():
    """Main entry point."""
    tests_dir = Path(__file__).parent
    
    runner = TestRunner(tests_dir)
    runner.run_all_tests()
    runner.print_summary()
    runner.print_recommendations()
    
    # Exit with appropriate code
    failed_count = sum(
        1 for r in runner.results.values()
        if r['status'] in ['FAILED', 'ERROR', 'TIMEOUT']
    )
    
    if failed_count > 0:
        print(f"\n{Color.RED}⚠️  {failed_count} Tests fehlgeschlagen{Color.NC}\n")
        sys.exit(1)
    else:
        print(f"\n{Color.GREEN}✅ Alle Tests abgeschlossen{Color.NC}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()

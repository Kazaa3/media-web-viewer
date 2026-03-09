#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Web Viewer - Comprehensive Build System

Handles building, testing, and packaging for multiple targets:
- Development builds
- PyInstaller executables
- Debian packages
- Distribution packages

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import sys
import os
import subprocess
import argparse
import shutil
import textwrap
from pathlib import Path
from typing import Optional


class BuildSystem:
    """Comprehensive build and test system for Media Web Viewer."""

    BUILD_TEST_GATE = [
        "tests/test_performance_probes.py",
        "tests/test_bottle_health_latency.py",
        "tests/test_installed_packages_ui.py",
        "tests/test_ui_session_stability.py",
    ]
    
    def __init__(self, root_dir: Optional[Path] = None):
        """
        Initialize build system.
        
        Args:
            root_dir: Project root directory (default: script parent dir)
        """
        self.root = root_dir or Path(__file__).parent
        self.version = self._read_version()
        
    def _read_version(self) -> str:
        """Read version from VERSION file."""
        version_file = self.root / "VERSION"
        if not version_file.exists():
            return "0.0.0"
        return version_file.read_text().strip()
    
    def _print_banner(self, title: str):
        """Print a formatted banner."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")
    
    def _run_command(self, cmd: list[str], cwd: Optional[Path] = None) -> bool:
        """
        Run a command and return success status.
        
        Args:
            cmd: Command and arguments as list
            cwd: Working directory (default: root)
            
        Returns:
            bool: True if command succeeded, False otherwise
        """
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.root,
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: {e}")
            if e.stderr:
                print(f"  stderr: {e.stderr}")
            return False
    
    def check_environment(self) -> bool:
        """
        Check that the build environment is properly configured.
        
        Returns:
            bool: True if environment is valid
        """
        self._print_banner("Environment Check")
        
        checks = {
            "Python >= 3.10": sys.version_info >= (3, 10),
            "requirements.txt exists": (self.root / "requirements.txt").exists(),
            "main.py exists": (self.root / "main.py").exists(),
            "web/ directory exists": (self.root / "web").is_dir(),
            "VERSION file exists": (self.root / "VERSION").exists(),
            "Browser available (Chrome/Chromium/Firefox)": self._check_browser_available(),
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}")
            if not passed:
                all_passed = False
        
        print()
        return all_passed

    def _check_browser_available(self) -> bool:
        """Check if at least one compatible browser is available."""
        browsers = ["google-chrome-stable", "google-chrome", "chrome", "chromium-browser", "chromium", "firefox"]
        return any(shutil.which(b) for b in browsers)
    
    def run_tests(self, verbose: bool = False) -> bool:
        """
        Run test suite using pytest.
        
        Args:
            verbose: Enable verbose output
            
        Returns:
            bool: True if all tests passed
        """
        self._print_banner(f"Running Tests (v{self.version})")
        
        cmd = [sys.executable, "-m", "pytest", "tests/"]
        if verbose:
            cmd.append("-v")
        
        return self._run_command(cmd)

    def run_build_test_gate(self, verbose: bool = False) -> bool:
        """
        Run the mandatory targeted pre-build quality gate.

        Args:
            verbose: Enable verbose output

        Returns:
            bool: True if gate passed
        """
        self._print_banner(f"Build Test Gate (v{self.version})")

        cmd = [sys.executable, "-m", "pytest"]
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")
        cmd.extend(self.BUILD_TEST_GATE)
        return self._run_command(cmd)
    
    def run_linter(self) -> bool:
        """
        Run code quality checks with flake8.
        
        Returns:
            bool: True if linting passed
        """
        self._print_banner("Code Quality Check (flake8)")
        
        cmd = [
            sys.executable, "-m", "flake8",
            "main.py", "db.py", "models.py", "logger.py", "env_handler.py",
            "--max-line-length=120",
            "--ignore=E501,W503"
        ]
        
        return self._run_command(cmd)
    
    def run_type_check(self) -> bool:
        """
        Run type checking with mypy.
        
        Returns:
            bool: True if type checking passed
        """
        self._print_banner("Type Checking (mypy)")
        
        cmd = [sys.executable, "-m", "mypy", "main.py", "db.py", "models.py"]
        
        return self._run_command(cmd)
    
    def build_pyinstaller(self, onefile: bool = True, console: bool = False, skip_build_gate: bool = False) -> bool:
        """
        Build standalone executable with PyInstaller.
        
        Args:
            onefile: Create single-file executable
            console: Show console window
            
        Returns:
            bool: True if build succeeded
        """
        self._print_banner(f"Building PyInstaller Executable (v{self.version})")

        if not skip_build_gate:
            if not self.run_build_test_gate():
                print("\n❌ Build test gate failed - aborting PyInstaller build")
                return False
        else:
            print("⚠️  Build test gate skipped (--skip-build-gate)")
        
        cmd = [
            sys.executable, "-m", "eel",
            "main.py", "web",
            "--clean",
            "--name", f"MediaWebViewer-{self.version}",
        ]
        
        if onefile:
            cmd.append("--onefile")
        
        if not console:
            cmd.append("--noconsole")
        
        success = self._run_command(cmd)
        
        if success:
            dist_dir = self.root / "dist"
            print(f"\n✅ Executable created in: {dist_dir}")
            if dist_dir.exists():
                for item in dist_dir.iterdir():
                    print(f"   - {item.name}")
        
        return success
    
    def build_debian_package(self, skip_build_gate: bool = False) -> bool:
        """
        Build Debian package using build_deb.sh script.
        
        Returns:
            bool: True if build succeeded
        """
        self._print_banner(f"Building Debian Package (v{self.version})")

        if not skip_build_gate:
            if not self.run_build_test_gate():
                print("\n❌ Build test gate failed - aborting Debian build")
                return False
        else:
            print("⚠️  Build test gate skipped (--skip-build-gate)")
        
        build_script = self.root / "build_deb.sh"
        if not build_script.exists():
            print("❌ build_deb.sh not found")
            return False
        
        cmd = ["bash", str(build_script)]
        if skip_build_gate:
            cmd = ["bash", "-lc", f"SKIP_BUILD_TESTS=1 bash '{build_script}'"]
        success = self._run_command(cmd)
        
        if success:
            deb_file = self.root / f"media-web-viewer_{self.version}_amd64.deb"
            if deb_file.exists():
                print(f"\n✅ Debian package created: {deb_file.name}")
                print(f"   Install: sudo dpkg -i {deb_file.name}")
        
        return success
    
    def clean(self, full: bool = False) -> bool:
        """
        Clean build artifacts.
        
        Args:
            full: Also remove dist/ and build/ directories
            
        Returns:
            bool: True if cleaning succeeded
        """
        self._print_banner("Cleaning Build Artifacts")
        
        patterns = [
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".pytest_cache",
            ".mypy_cache",
            "*.egg-info",
        ]
        
        removed: list[str] = []
        
        # Remove pattern-based artifacts
        for pattern in patterns:
            for item in self.root.rglob(pattern):
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    removed.append(str(item.relative_to(self.root)))
                except Exception as e:
                    print(f"⚠️ Could not remove {item}: {e}")
        
        # Remove build directories if full clean
        if full:
            for dir_name in ["build", "dist"]:
                dir_path = self.root / dir_name
                if dir_path.exists():
                    shutil.rmtree(dir_path)
                    removed.append(dir_name + "/")
        
        if removed:
            print("Removed:")
            for item in removed[:10]:  # Show first 10
                print(f"  - {item}")
            if len(removed) > 10:
                print(f"  ... and {len(removed) - 10} more")
        else:
            print("No artifacts to clean")
        
        print("\n✅ Clean complete")
        return True
    
    def show_info(self):
        """Display project information."""
        self._print_banner("Project Information")
        
        print(f"Project: Media Web Viewer")
        print(f"Version: {self.version}")
        print(f"Root: {self.root}")
        print(f"Python: {sys.version.split()[0]} ({sys.executable})")
        
        # Count files
        py_files = list(self.root.glob("*.py"))
        test_files = list((self.root / "tests").glob("*.py")) if (self.root / "tests").exists() else []
        
        print(f"\nFiles:")
        print(f"  Python modules: {len(py_files)}")
        print(f"  Test files: {len(test_files)}")
        
        # Check dependencies
        req_file = self.root / "requirements.txt"
        if req_file.exists():
            requirements = [line.strip() for line in req_file.read_text().splitlines()
                          if line.strip() and not line.startswith('#')]
            print(f"  Dependencies: {len(requirements)}")
        
        print()
    
    def full_build(self, target: str = "deb", skip_tests: bool = False, skip_build_gate: bool = False) -> bool:
        """
        Complete build process: test, check, and build.
        
        Args:
            target: Build target ('deb', 'pyinstaller', or 'all')
            skip_tests: Skip test execution
            
        Returns:
            bool: True if entire build succeeded
        """
        self._print_banner(f"Full Build Process - v{self.version}")
        
        print(f"Target: {target}")
        print(f"Skip tests: {skip_tests}\n")
        
        # Step 1: Environment check
        if not self.check_environment():
            print("❌ Environment check failed")
            return False
        
        # Step 2: Run tests
        if not skip_tests:
            if not self.run_tests():
                print("\n❌ Tests failed - aborting build")
                return False
        else:
            print("⚠️  Tests skipped")
        
        # Step 3: Build based on target
        if target == "deb":
            success = self.build_debian_package(skip_build_gate=skip_build_gate)
        elif target == "pyinstaller":
            success = self.build_pyinstaller(skip_build_gate=skip_build_gate)
        elif target == "all":
            success = self.build_pyinstaller(skip_build_gate=skip_build_gate) and self.build_debian_package(skip_build_gate=skip_build_gate)
        else:
            print(f"❌ Unknown target: {target}")
            return False
        
        if success:
            self._print_banner("✅ Build Complete!")
            print(f"Version: {self.version}")
            print(f"Target: {target}")
        else:
            print("\n❌ Build failed")
        
        return success

    def run_pipeline(self, destructive: bool = False, skip_build_gate: bool = False) -> bool:
        """
        Run release pipeline checks and build artifacts.

        Pipeline steps:
        1) Environment check
        2) Version sync validation
        3) Build Debian package (includes build gate by default)
        4) Reinstall validation tests (safe)
        5) Optional destructive reinstall validation
        """
        self._print_banner(f"Release Pipeline - v{self.version}")

        print(f"Destructive checks: {destructive}\n")

        if not self.check_environment():
            print("❌ Environment check failed")
            return False

        print("▶ Step 1/4: Version synchronization check")
        if not self._run_command([sys.executable, "tests/test_version_sync.py"]):
            print("\n❌ Version sync failed")
            return False

        print("▶ Step 2/4: Build Debian package")
        if not self.build_debian_package(skip_build_gate=skip_build_gate):
            print("\n❌ Debian build failed")
            return False

        print("▶ Step 3/4: Reinstall validation (safe)")
        if not self._run_command([sys.executable, "tests/test_reinstall_deb.py"]):
            print("\n❌ Reinstall validation failed")
            return False

        if destructive:
            print("▶ Step 4/4: Reinstall validation (destructive)")
            cmd = [
                "bash",
                "-lc",
                f"RUN_DESTRUCTIVE_TESTS=1 {sys.executable} tests/test_reinstall_deb.py"
            ]
            if not self._run_command(cmd):
                print("\n❌ Destructive reinstall validation failed")
                return False
        else:
            print("▶ Step 4/4: Destructive reinstall validation skipped")

        self._print_banner("✅ Pipeline Complete")
        print(f"Version: {self.version}")
        print("All pipeline steps passed.")
        return True


def main():
    """Main entry point for build system CLI."""
    parser = argparse.ArgumentParser(
        description="Media Web Viewer Build System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=textwrap.dedent("""
                        Examples:
                            %(prog)s --info                          Show project information
                            %(prog)s --test                          Run tests only
                            %(prog)s --build deb                     Build Debian package
                            %(prog)s --build pyinstaller             Build PyInstaller executable
                            %(prog)s --build all                     Build all targets
                            %(prog)s --full-build                    Full build with tests
                            %(prog)s --full-build --skip-build-gate Skip targeted pre-build gate in full build
                            %(prog)s --pipeline                      Run release pipeline (sync + build + reinstall tests)
                            %(prog)s --pipeline --destructive        Include destructive reinstall test
                            %(prog)s --pipeline --skip-build-gate    Skip targeted pre-build gate in pipeline build step
                            %(prog)s --clean                         Clean build artifacts
                            %(prog)s --clean-all                     Deep clean (includes dist/)
                """)
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show project information"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test suite"
    )
    
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Run code quality checks"
    )
    
    parser.add_argument(
        "--type-check",
        action="store_true",
        help="Run type checking"
    )
    
    parser.add_argument(
        "--build",
        choices=["deb", "pyinstaller", "all"],
        help="Build target"
    )
    
    parser.add_argument(
        "--full-build",
        action="store_true",
        help="Complete build process (test + check + build)"
    )

    parser.add_argument(
        "--pipeline",
        action="store_true",
        help="Run release pipeline (version sync, deb build, reinstall validation)"
    )

    parser.add_argument(
        "--destructive",
        action="store_true",
        help="Enable destructive checks (used with --pipeline)"
    )
    
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip tests in full build"
    )

    parser.add_argument(
        "--skip-build-gate",
        action="store_true",
        help="Skip targeted pre-build gate tests for build/pipeline commands"
    )
    
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build artifacts"
    )
    
    parser.add_argument(
        "--clean-all",
        action="store_true",
        help="Deep clean (includes dist/ and build/)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    
    # Initialize build system
    build_sys = BuildSystem()
    
    success = True
    
    # Execute requested actions
    if args.info:
        build_sys.show_info()
    
    if args.clean or args.clean_all:
        success = build_sys.clean(full=args.clean_all) and success
    
    if args.test:
        success = build_sys.run_tests(verbose=args.verbose) and success
    
    if args.lint:
        success = build_sys.run_linter() and success
    
    if args.type_check:
        success = build_sys.run_type_check() and success
    
    if args.build:
        if args.build == "deb":
            success = build_sys.build_debian_package(skip_build_gate=args.skip_build_gate) and success
        elif args.build == "pyinstaller":
            success = build_sys.build_pyinstaller(skip_build_gate=args.skip_build_gate) and success
        elif args.build == "all":
            success = build_sys.build_pyinstaller(skip_build_gate=args.skip_build_gate) and build_sys.build_debian_package(skip_build_gate=args.skip_build_gate) and success
    
    if args.full_build:
        success = build_sys.full_build(target="deb", skip_tests=args.skip_tests, skip_build_gate=args.skip_build_gate) and success

    if args.pipeline:
        success = build_sys.run_pipeline(destructive=args.destructive, skip_build_gate=args.skip_build_gate) and success
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

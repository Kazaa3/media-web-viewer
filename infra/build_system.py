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
import platform
import subprocess
import time
import shutil
import argparse
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

# Ensure scripts directory is in path for monitor_utils
ROOT_PATH = Path(__file__).resolve().parent.parent
SCRIPTS_PATH = ROOT_PATH / "scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.append(str(SCRIPTS_PATH))

import monitor_utils  # type: ignore
from status_bar_utils import StatusBar  # type: ignore


def print_status(message: str, category: str = "INFO"):
    """Print a formatted status message."""
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "PROCESS": "⚙️"}
    icon = icons.get(category, "•")
    print(f"{icon} {message}")


class BuildSystem:
    """Comprehensive build and test system for Media Web Viewer."""

    BUILD_TEST_GATE = [
        "tests/integration/performance/test_performance_probes.py",
        "tests/integration/tech/bottle/test_bottle_health_latency.py",
        "tests/integration/category/ui/test_installed_packages_ui.py",
        "tests/integration/basic/env/test_environment_packages_fallback.py",
        "tests/integration/category/ui/test_ui_session_stability.py",
        "tests/integration/category/git/test_git_guard.py",
    ]

    TEST_TIERS = {
        "unit": "tests/unit/",
        "integration": "tests/integration/",
        "e2e": "tests/e2e/",
        "all": "tests/"
    }

    import contextlib

    @contextlib.contextmanager
    def timer(self, phase_name: str):
        """Context manager to measure and log phase duration."""
        start = time.time()
        print_status(f"Starting phase: {phase_name}", "PROCESS")
        try:
            yield
        finally:
            end = time.time()
            duration = end - start
            self.metrics.append({"phase": phase_name, "duration": duration})
            print_status(f"Finished {phase_name} in {duration:.2f}s", "SUCCESS")

    def __init__(self, root_dir: Optional[Path] = None):
        """
        Initialize build system.

        Args:
            root_dir: Project root directory (default: script parent dir)
        """
        self.root = root_dir or Path(__file__).resolve().parent.parent
        self.version = self._read_version()
        self.metrics = []
        self.start_time = time.time()
        
        # Setup management reports directory
        self.reports_dir = self.root / "build" / "management_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.build_dir = self.root / "build"
        self.dist_dir = self.root / "dist"
        
        self.branch = self._get_current_branch()

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

    def clean(self, full: bool = False):
        """Clean build and temporary directories."""
        self._print_banner("Cleaning Build Artifacts")
        
        folders_to_clean = [
            self.root / "build" / "pyinstaller_work",
            self.root / "build" / "deb_staging",
            self.dist_dir,
            self.root / ".pytest_cache"
        ]
        
        if full:
            print_status("Removing all build artifacts and reports...", "WARNING")
            folders_to_clean.append(self.reports_dir)
            folders_to_clean.append(self.build_dir)
            
        for folder in folders_to_clean:
            if folder.exists():
                print_status(f"Removing {folder.relative_to(self.root)}...", "INFO")
                try:
                    shutil.rmtree(folder)
                except Exception as e:
                    print_status(f"Error removing {folder}: {e}", "WARNING")
        
        # Re-ensure reports dir if it was wiped
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def _get_current_branch(self) -> str:
        """Detect the current git branch."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"

    def deploy_branch_config(self) -> bool:
        """Deploy branch-specific configuration JSON."""
        print_status(f"Deploying config for branch: {self.branch}", "PROCESS")
        
        config_src = self.root / "web" / f"config.{self.branch}.json"
        config_dest = self.root / "web" / "config.json"
        
        # Fallback to dev if specialized branch config doesn't exist
        if not config_src.exists():
            if "milestone" in self.branch or self.branch == "develop":
                 config_src = self.root / "web" / "config.develop.json"
            else:
                 config_src = self.root / "web" / "config.main.json"

        if config_src.exists():
            shutil.copy2(config_src, config_dest)
            print_status(f"Deployed {config_src.name} -> {config_dest.name}", "SUCCESS")
            return True
        else:
            print_status(f"No specific config found for {self.branch}, using legacy default if exists", "WARNING")
            return True # Not a hard failure

    def _run_command(
            self,
            cmd: list[str],
            cwd: Optional[Path] = None,
            monitor: bool = False,
            **kwargs) -> bool:
        """
        Run a command and return success status.
        """
        start_time = time.time()
        timeout = kwargs.get("timeout", 600)  # Default 10 min timeout

        if not monitor:
            try:
                result = subprocess.run(
                    cmd,
                    cwd=cwd or self.root,
                    env=kwargs.get("env"),
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                duration = time.time() - start_time
                self.metrics.append(
                    {"cmd": cmd[0], "duration": duration, "status": "success"})
                if result.stdout:
                    print(result.stdout)
                return True
            except subprocess.TimeoutExpired:
                print(f"❌ Timeout Error: Command '{cmd[0]}' timed out after {timeout}s")
                self.metrics.append(
                    {"cmd": cmd[0], "duration": timeout, "status": "timeout"})
                return False
            except subprocess.CalledProcessError as e:
                duration = time.time() - start_time
                print(f"❌ Error: {e}")
                self.metrics.append(
                    {"cmd": cmd[0], "duration": duration, "status": "failed"})
                if e.stdout:
                    print(f"  stdout: {e.stdout}")
                if e.stderr:
                    print(f"  stderr: {e.stderr}")
                return False
        else:
            try:
                from monitor_utils import run_monitored
                success = run_monitored(
                    cmd,
                    cwd=str(cwd or self.root),
                    env=kwargs.get("env"),
                    hang_timeout=kwargs.get("hang_timeout", 300),
                    alive_interval=kwargs.get("alive_interval", 30)
                )
                duration = time.time() - start_time
                self.metrics.append(
                    {"cmd": cmd[0], "duration": duration, "status": "success" if success else "failed/hang"})
                return success
            except ImportError:
                print_status(
                    "monitor_utils not found, falling back to standard execution",
                    "WARNING")
                return self._run_command(cmd, cwd=cwd, monitor=False, **kwargs)

    def check_environment(self) -> bool:
        """
        Check that the build environment is properly configured.

        Returns:
            bool: True if environment is valid
        """
        self._print_banner("Environment Check")

        checks = {
            "Python >= 3.10": sys.version_info >= (3, 10),
            "requirements.txt exists": (self.root / "infra" / "requirements.txt").exists(),
            "main.py exists": (self.root / "src/core/main.py").exists(),
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
        browsers = [
            "google-chrome-stable",
            "google-chrome",
            "chrome",
            "chromium-browser",
            "chromium",
            "firefox"]
        return any(shutil.which(b) for b in browsers)

    def run_tests(
            self,
            tier: str,
            verbose: bool = False,
            report: bool = False) -> bool:
        """Run tests for a specified tier."""
        with self.timer(f"Testing ({tier})"):
            if tier not in self.TEST_TIERS:
                print(f"❌ Error: Unknown test tier '{tier}'")
                return False
            self._print_banner(f"Running {tier.upper()} Tests")

            test_paths = {
                "unit": "tests/unit",
                "integration": "tests/integration",
                "e2e": "tests/e2e",
                "all": "tests"
            }

            path = test_paths.get(tier)
            if not path:
                print(f"❌ Unknown test tier: {tier}")
                return False

            cmd = [sys.executable, "-m", "pytest", path]
            if verbose:
                cmd.append("-v")

            if report:
                report_file = self.reports_dir / f"report-{tier}.xml"
                cmd.extend(["--junitxml", str(report_file)])
                print_status(f"Reporting to: {report_file}", "INFO")

            success = self._run_command(cmd)

            if report and report_file.exists():
                self._print_test_summary(report_file)

            return success

    def _print_test_summary(self, xml_file: Path):
        """Parse JUnit XML and print a summary."""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # handle both single testsuite and multiple testsuites
            if root.tag == 'testsuites':
                suites = root.findall('testsuite')
            else:
                suites = [root]

            total = 0
            failures = 0
            errors = 0
            skipped = 0
            time_taken = 0.0

            for s in suites:
                total += int(s.get('tests', 0))
                failures += int(s.get('failures', 0))
                errors += int(s.get('errors', 0))
                skipped += int(s.get('skipped', 0))
                time_taken += float(s.get('time', 0.0))

            passed = total - failures - errors - skipped

            print("\n" + "═" * 40)
            print("         TEST RESULT SUMMARY")
            print("═" * 40)
            print(f"  Total:    {total}")
            print(f"  Passed:   {
                  passed} ({(passed / total * 100 if total > 0 else 0):.1f}%)")
            if failures:
                print(f"  Failures: {failures}")
            if errors:
                print(f"  Errors:   {errors}")
            if skipped:
                print(f"  Skipped:  {skipped}")
            print(f"  Duration: {time_taken:.2f}s")
            print("═" * 40 + "\n")

        except Exception as e:
            print(f"⚠️ Could not parse test report: {e}")

    def run_build_test_gate(self, verbose: bool = False, report: bool = True) -> bool:
        """
        Run the mandatory targeted pre-build quality gate.

        Args:
            verbose: Enable verbose output
            report: Enable JUnit XML reporting

        Returns:
            bool: True if gate passed
        """
        self._print_banner(f"Build Test Gate (v{self.version})")

        cmd = [sys.executable, "-m", "pytest"]
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")

        if report:
            report_file = self.reports_dir / "report-gate.xml"
            cmd.extend(["--junitxml", str(report_file)])
            print_status(f"Reporting gate results to: {report_file}", "INFO")

        cmd.extend(self.BUILD_TEST_GATE)
        success = self._run_command(cmd)

        if report and report_file.exists():
            self._print_test_summary(report_file)

        return success

    def run_linter(self) -> bool:
        """
        Run code quality checks with flake8.

        Returns:
            bool: True if linting passed
        """
        self._print_banner("Code Quality Check (flake8)")

        cmd = [
            sys.executable, "-m", "flake8",
            "src/core/main.py", "src/core/db.py", "src/core/models.py",
            "src/core/logger.py", "src/core/env_handler.py",
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

        cmd = [
            sys.executable,
            "-m",
            "mypy",
            "src/core/main.py",
            "src/core/db.py",
            "src/core/models.py"]

        return self._run_command(cmd)

    def build_pyinstaller(
            self,
            onefile: bool = True,
            console: bool = False,
            skip_build_gate: bool = False,
            **kwargs) -> bool:
        """
        Build standalone executable with PyInstaller.

        Args:
            onefile: Create single-file executable
            console: Show console window
            monitor: Enable robust hang detection (passed via **kwargs)

        Returns:
            bool: True if build succeeded
        """
        with self.timer("Windows EXE Build"):
            self._print_banner(
                f"Building PyInstaller Executable (v{
                    self.version})")

            if not skip_build_gate:
                if not self.run_build_test_gate():
                    print("\n❌ Build test gate failed - aborting PyInstaller build")
                    return False
            else:
                print("⚠️  Build test gate skipped (--skip-build-gate)")

            # Use the consolidated spec file
            spec_file = self.root / "infra" / "packaging" / "specs" / "MediaWebViewer.spec"
            if not spec_file.exists():
                 # Fallback to general spec if specific one not found
                 spec_file = self.root / "infra" / "packaging" / "specs" / f"MediaWebViewer-{self.version}.spec"
            
            if not spec_file.exists():
                print_status(f"Critical: Spec file not found at {spec_file}", "ERROR")
                return False

            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--clean",
                str(spec_file),
                "--workpath", str(self.root / "build" / "pyinstaller_work"),
                "--distpath", str(self.root / "dist")
            ]

            success = self._run_command(
                cmd, monitor=kwargs.get(
                    "monitor", False), hang_timeout=900)

            # Post-build verification: Check artifact version naming
            if success:
                expected_artifact = self.root / "dist" / \
                    f"MediaWebViewer-{self.version}"
                if platform.system() == "Windows":
                    expected_artifact = expected_artifact.with_suffix(".exe")

                if not expected_artifact.exists():
                    print_status(
                        f"Versioning Mismatch: Expected artifact {
                            expected_artifact.name} not found!", "ERROR")
                    # Audit dist dir for what actually was built
                    actual_items = list(
                        (self.root /
                         "dist").iterdir()) if (
                        self.root /
                        "dist").exists() else []
                    print(
                        f"   Found in dist/: {[item.name for item in actual_items]}")
                    return False

            if success:
                dist_dir = self.root / "dist"
                print(f"\n✅ Executable created in: {dist_dir}")
                if dist_dir.exists():
                    for item in dist_dir.iterdir():
                        print(f"   - {item.name}")

            return success

    def print_summary(self):
        """Print a summary of the entire build/test session."""
        total_duration = time.time() - self.start_time
        self._print_banner("BUILD SESSION SUMMARY")

        print(f"  Version:        {self.version}")
        print(f"  Total Duration: {total_duration:.2f}s")
        print("\n  Phase Durations:")

        for metric in self.metrics:
            if "phase" in metric:
                print(f"    - {metric['phase']
                      :<20}: {metric['duration']:.2f}s")
            elif "cmd" in metric:
                status = metric.get("status", "unknown")
                print(f"    - [Cmd] {metric['cmd']
                      :<14}: {metric['duration']:.2f}s ({status})")

        print("\n" + "=" * 70 + "\n")

    def build_deb(self) -> bool:
        """Build Debian package."""
        with self.timer("Debian Build"):
            self._print_banner(f"Building Debian Package (v{self.version})")

            # Use build_deb.sh script
            script = self.root / "infra" / "build_deb.sh"
            if not script.exists():
                print("Performance Benchmark suite not found locally.")
                return False

            return self._run_command(["bash", str(script)], monitor=True)

    def run_performance_benchmarks(self) -> bool:
        """
        Run all performance benchmarks in tests/advanced/performance/.
        """
        self._print_banner("Running Performance Benchmarks")

        benchmark_files = [
            "tests/integration/performance/benchmark_debug_db_write_speed.py",
            "tests/integration/performance/benchmark_scanner.py",
            "tests/integration/performance/compare_benchmarks.py",
            "tests/integration/performance/test_performance_probes.py",
            "tests/integration/performance/test_transcoding_performance_debug.py",
            "tests/integration/tech/ffmpeg/benchmark_all_parsers.py"]

        all_success = True
        total_benchmarks = len(benchmark_files)
        
        with StatusBar("Performance Benchmarks", total=total_benchmarks) as sb:
            for i, bench in enumerate(benchmark_files, 1):
                file_path = self.root / bench
                if not file_path.exists():
                    print(f"\r⚠️ Benchmark missing: {bench}")
                    continue

                sb.update(i, f"(Running {bench})")
                
                # Benchmarks can be heavy, use monitoring by default for them
                env = os.environ.copy()
                env["PYTHONPATH"] = str(self.root)
                env["PERF_REPORT_DIR"] = str(self.reports_dir)
                
                # Watchdog: monitor the debug log for progress if the benchmark writes to it
                debug_log = self.root / "data" / "logs" / "debug.log"
                
                # We capture output to avoid breaking the status bar
                if not self._run_command(
                    [sys.executable, str(file_path)], 
                    monitor=True, 
                    hang_timeout=300, 
                    env=env,
                    watch_files=[str(debug_log)] if debug_log.exists() else None,
                    watch_timeout=180
                ):
                    all_success = False
            sb.update(i, f"(Finished {bench})")

        return all_success

    def run_performance_audit(self) -> bool:
        """
        Run a comprehensive performance audit of all parsers.
        """
        self._print_banner("Running Performance Audit")

        audit_script = "tests/integration/tech/ffmpeg/benchmark_all_parsers.py"
        file_path = self.root / audit_script

        if not file_path.exists():
            print_status(f"Audit script missing: {audit_script}", "ERROR")
            return False

        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root)
        env["PERF_REPORT_DIR"] = str(self.reports_dir)

        print_status(f"Executing audit: {audit_script}", "PROCESS")
        success = self._run_command([sys.executable, str(file_path)], monitor=True, env=env)

        if success:
            print_status(f"Audit report generated in {self.reports_dir}", "SUCCESS")

        return success

    def build_debian_package(
            self,
            skip_build_gate: bool = False,
            install: bool = False,
            monitor: bool = False) -> bool:
        """
        Build a Debian package.
        """
        self._print_banner(f"Building Debian Package (v{self.version})")

        # Deploy branch-specific config before building
        self.deploy_branch_config()

        # Args:
        #     skip_build_gate: Skip pre-build gate
        #     install: Automatically install/reinstall after build
        #     **kwargs: monitor, hang_timeout

        # Returns:
        #     bool: True if build succeeded
        # """
        with self.timer("Debian Build"):
            # self._print_banner(f"Building Debian Package (v{self.version})")

            if not skip_build_gate:
                if not self.run_build_test_gate():
                    print("\n❌ Build test gate failed - aborting Debian build")
                    return False
            else:
                print("⚠️  Build test gate skipped (--skip-build-gate)")

            build_script = self.root / "infra" / "build_deb.sh"
            if not build_script.exists():
                print("❌ build_deb.sh not found")
                return False

            # Avoid duplicate gate execution
            env = os.environ.copy()
            env["SKIP_BUILD_TESTS"] = "1"

            # Determine if we should use monitoring
            # monitor = kwargs.get("monitor", False)

            cmd = ["bash", "-lc", f"BRANCH={self.branch} SKIP_BUILD_TESTS=1 bash '{build_script}'"]
            success = self._run_command(cmd, monitor=monitor, hang_timeout=600)

            if success:
                deb_file = self.root / \
                    f"media-web-viewer_{self.version}_amd64.deb"
                if deb_file.exists():
                    print(f"\n✅ Debian package created: {deb_file.name}")

                    if install:
                        print_status(
                            "Automatically installing package...", "PROCESS")
                        reinstall_script = self.root / "scripts" / "reinstall_deb.sh"
                        if reinstall_script.exists():
                            self._run_command(["bash", str(reinstall_script)])
                        else:
                            print("❌ reinstall_deb.sh not found for auto-install")
                    else:
                        print(f"   Install: sudo dpkg -i {deb_file.name}")

            return success

    def sync_environments(
            self,
            target: str = "all",
            force: bool = False) -> bool:
        """
        Sync virtual environments using manage_venvs.py.
        """
        self._print_banner("Synchronizing Virtual Environments")
        manage_script = self.root / "scripts" / "manage_venvs.py"
        if not manage_script.exists():
            print("❌ manage_venvs.py not found")
            return False

        cmd = [sys.executable, str(manage_script), "--sync", target]
        if force:
            cmd.append("--force")

        return self._run_command(cmd)

    def clean_fragments(self) -> bool:
        """Clean all temporary build/test fragments across the project."""
        self._print_banner("Cleaning Temporary Fragments")

        # 1. Use manage_venvs for its fragments
        manage_script = self.root / "scripts" / "manage_venvs.py"
        if manage_script.exists():
            self._run_command([sys.executable, str(
                manage_script), "--clean-fragments"])

        # 2. Clean infra/packaging fragments
        pkg_staging = self.root / "infra" / "packaging" / "opt"
        if pkg_staging.exists():
            print_status(f"Cleaning pkg staging: {pkg_staging}", "PROCESS")
            for item in pkg_staging.iterdir():
                if item.name == ".gitkeep":
                    continue
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

        return True

    def clean(self, full: bool = False) -> bool:
        """Clean build artifacts and temporary files."""
        with self.timer("Clean"):
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

            if full:
                patterns.extend(["*.deb", "*.exe"])

        removed: list[str] = []

        # 1. Remove pattern-based artifacts
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

        # 2. Remove build directories if full clean
        if full:
            for dir_name in [
                "build",
                "dist",
                    "infra/packaging/opt/media-web-viewer"]:
                dir_path = self.root / dir_name
                if dir_path.exists():
                    try:
                        shutil.rmtree(dir_path)
                        removed.append(dir_name + "/")
                    except Exception as e:
                        print(f"⚠️ Could not remove {dir_path}: {e}")

        # 3. Explicitly clean fragments too
        self.clean_fragments()

        if removed:
            print(f"\n✅ Clean complete. Removed {len(removed)} items.")
        else:
            print("\n✅ Tree is already clean.")
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
        test_files = list((self.root / "tests").glob("*.py")
                          ) if (self.root / "tests").exists() else []

        print(f"\nFiles:")
        print(f"  Python modules: {len(py_files)}")
        print(f"  Test files: {len(test_files)}")

        # Check dependencies
        req_file = self.root / "requirements.txt"
        if req_file.exists():
            requirements = [line.strip() for line in req_file.read_text(
            ).splitlines() if line.strip() and not line.startswith('#')]
            print(f"  Dependencies: {len(requirements)}")

        print()

    def full_build(
            self,
            target: str = "deb",
            skip_tests: bool = False,
            skip_build_gate: bool = False,
            **kwargs) -> bool:
        """Complete build process: test, check, and build."""
        with self.timer(f"Full Build ({target})"):
            self._print_banner(f"Full Build Process - v{self.version}")

            print(f"Target: {target}")
            print(f"Skip tests: {skip_tests}\n")

            # Step 1: Environment check
            if not self.check_environment():
                print("❌ Environment check failed")
                return False

            # Step 2: Run tests
            if not skip_tests:
                if not self.run_tests(
                    tier="all", verbose=kwargs.get(
                        "verbose", False), report=kwargs.get(
                        "report", False)):
                    print("\n❌ Tests failed - aborting build")
                    return False
            else:
                print("⚠️  Tests skipped")

            # Step 3: Build based on target
            success = False
            if target == "deb":
                success = self.build_debian_package(
                    skip_build_gate=skip_build_gate, install=kwargs.get(
                        "install", False))
            elif target == "pyinstaller":
                success = self.build_pyinstaller(
                    skip_build_gate=skip_build_gate)
            elif target == "all":
                success = self.build_pyinstaller(
                    skip_build_gate=skip_build_gate) and self.build_debian_package(
                    skip_build_gate=skip_build_gate, install=kwargs.get(
                        "install", False))
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

    def run_pipeline(
            self,
            destructive: bool = False,
            skip_build_gate: bool = False) -> bool:
        """
        Run the full release pipeline.
        """
        self._print_banner(f"Release Pipeline - v{self.version}")
        
        # Deploy branch-specific config
        self.deploy_branch_config()
        with self.timer("Pipeline Build"):
            if not self.check_environment():
                print("❌ Environment check failed")
                return False

            print("▶ Step 1/4: Version synchronization check")
            if not self._run_command(
                    [sys.executable, "tests/integration/test_version_sync.py"]):
                print("\n❌ Version sync failed")
                return False

            print("▶ Step 2/4: Build Debian package")
            if not self.build_debian_package(
                    skip_build_gate=skip_build_gate,
                    install=destructive):
                print("\n❌ Debian build failed")
                return False

            print("▶ Step 3/4: Reinstall validation (safe)")
            if not self._run_command(
                    [sys.executable, "tests/e2e/install/test_reinstall_deb.py"]):
                print("\n❌ Reinstall validation failed")
                return False

            if destructive:
                print("▶ Step 4/4: Reinstall validation (destructive)")
                cmd = [
                    "bash",
                    "-lc",
                    f"RUN_DESTRUCTIVE_TESTS=1 {
                        sys.executable} tests/e2e/install/test_reinstall_deb.py"]
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
        choices=["unit", "integration", "e2e", "all"],
        help="Run a specific test tier"
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
        choices=["deb", "exe", "all"],
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
        help="Run release pipeline (version sync, deb build, reinstall validation)")

    parser.add_argument(
        "--destructive",
        action="store_true",
        help="Enable destructive checks (used with --pipeline)"
    )

    parser.add_argument(
        "--benchmarks",
        action="store_true",
        help="Run performance benchmarks"
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
        "--monitor",
        action="store_true",
        help="Enable robust hang detection and monitoring"
    )

    parser.add_argument(
        "--sync-envs",
        nargs="?",
        const="all",
        help="Sync virtual environments (e.g. all, .venv_core, venv)"
    )

    parser.add_argument(
        "--install",
        action="store_true",
        help="Automatically install/reinstall Debian package after build"
    )

    parser.add_argument(
        "--clean-fragments",
        action="store_true",
        help="Clean temporary build/test fragments"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force action (e.g. force venv recreation)"
    )

    parser.add_argument(
        "--clean-all",
        action="store_true",
        help="Deep clean (includes dist/ and build/)"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate JUnit XML test reports in build/test-reports/"
    )

    parser.add_argument(
        "--test-gate",
        action="store_true",
        help="Run targeted pre-build gate tests"
    )

    parser.add_argument(
        "--deploy-config",
        action="store_true",
        help="Deploy branch-specific configuration to web/config.json"
    )

    parser.add_argument(
        "--audit-performance",
        action="store_true",
        help="Run comprehensive parser performance audit with format statistics"
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
        success = build_sys.run_tests(
            tier=args.test,
            verbose=args.verbose,
            report=args.report) and success

    if args.lint:
        success = build_sys.run_linter() and success

    if args.test_gate:
        success = build_sys.run_build_test_gate(verbose=args.verbose) and success

    if args.type_check:
        success = build_sys.run_type_check() and success

    if args.sync_envs:
        success = build_sys.sync_environments(
            target=args.sync_envs, force=args.force) and success

    if args.clean_fragments:
        success = build_sys.clean_fragments() and success

    if args.benchmarks:
        success = build_sys.run_performance_benchmarks() and success

    if args.build:
        if args.build == "deb":
            success = build_sys.build_debian_package(
                skip_build_gate=args.skip_build_gate,
                install=args.install,
                monitor=args.monitor) and success
        elif args.build == "pyinstaller":
            success = build_sys.build_pyinstaller(
                skip_build_gate=args.skip_build_gate,
                monitor=args.monitor) and success
        elif args.build == "all":
            success = build_sys.build_pyinstaller(
                skip_build_gate=args.skip_build_gate,
                monitor=args.monitor) and build_sys.build_debian_package(
                skip_build_gate=args.skip_build_gate,
                install=args.install,
                monitor=args.monitor) and success

    if args.full_build:
        success = build_sys.full_build(
            target="deb",
            skip_tests=args.skip_tests,
            skip_build_gate=args.skip_build_gate,
            install=args.install,
            monitor=args.monitor) and success

    if args.pipeline:
        success = build_sys.run_pipeline(
            destructive=args.destructive,
            skip_build_gate=args.skip_build_gate) and success

    if args.deploy_config:
        success = build_sys.deploy_branch_config() and success

    if args.audit_performance:
        success = build_sys.run_performance_audit() and success

    # Final summary
    build_sys.print_summary()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

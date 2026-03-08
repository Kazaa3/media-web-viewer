#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for version synchronization across the project.
Reads VERSION_SYNC.json and verifies all locations have the correct version.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class VersionSyncTester:
    """Test version synchronization across project files."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.version_file = project_root / "VERSION"
        self.sync_file = project_root / "VERSION_SYNC.json"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def load_master_version(self) -> str:
        """Load the master version from VERSION file."""
        if not self.version_file.exists():
            raise FileNotFoundError(f"VERSION file not found: {self.version_file}")
        
        version = self.version_file.read_text(encoding='utf-8').strip()
        print(f"📌 Master version from VERSION file: {version}")
        return version
    
    def load_sync_config(self) -> Dict:
        """Load the version synchronization configuration."""
        if not self.sync_file.exists():
            raise FileNotFoundError(f"VERSION_SYNC.json not found: {self.sync_file}")
        
        with open(self.sync_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"📋 Loaded sync config: {len(config['sync_locations'])} locations to check")
        return config
    
    def validate_version_format(self, version: str, pattern: str) -> bool:
        """Validate version string against regex pattern."""
        if re.match(pattern, version):
            print(f"✅ Version format valid: {version} matches {pattern}")
            return True
        else:
            self.errors.append(f"Version format invalid: {version} doesn't match {pattern}")
            return False
    
    def check_location(self, location: Dict, master_version: str) -> bool:
        """Check if a specific location has the correct version."""
        file_path = self.project_root / location['file']
        expected_pattern = location['line_pattern'].replace('${version}', master_version)
        description = location['description']
        required = location.get('required', True)
        note = location.get('note', '')
        
        print(f"\n🔍 Checking: {location['file']}")
        print(f"   Description: {description}")
        if note:
            print(f"   Note: {note}")
        
        # Check if file exists
        if not file_path.exists():
            error_msg = f"File not found: {location['file']}"
            if required:
                self.errors.append(error_msg)
                print(f"   ❌ {error_msg}")
                return False
            else:
                self.warnings.append(error_msg)
                print(f"   ⚠️  {error_msg} (optional)")
                return True
        
        # Read file and search for pattern
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # For exact pattern matching
            if expected_pattern in content:
                print(f"   ✅ Version OK: Found '{expected_pattern}'")
                return True
            
            # Try to find the version number in the file for debugging
            version_pattern = re.escape(master_version)
            matches = re.findall(f".*{version_pattern}.*", content)
            
            if matches:
                print(f"   ❌ Version found but pattern doesn't match!")
                print(f"      Expected: {expected_pattern}")
                print(f"      Found: {matches[0].strip() if matches else 'N/A'}")
                self.errors.append(
                    f"{location['file']}: Expected '{expected_pattern}' but found '{matches[0].strip() if matches else 'N/A'}'"
                )
            else:
                print(f"   ❌ Version {master_version} not found in file!")
                print(f"      Expected pattern: {expected_pattern}")
                self.errors.append(
                    f"{location['file']}: Version {master_version} not found"
                )
            
            return False
            
        except Exception as e:
            error_msg = f"Error reading {location['file']}: {e}"
            self.errors.append(error_msg)
            print(f"   ❌ {error_msg}")
            return False
    
    def check_version_sync_consistency(self, config: Dict, master_version: str) -> bool:
        """Check if VERSION_SYNC.json version matches VERSION file."""
        config_version = config.get('version', '')
        
        print(f"\n🔄 Checking VERSION_SYNC.json consistency...")
        print(f"   VERSION file: {master_version}")
        print(f"   VERSION_SYNC.json: {config_version}")
        
        if config_version == master_version:
            print(f"   ✅ VERSION_SYNC.json is up to date")
            return True
        else:
            self.errors.append(
                f"VERSION_SYNC.json version ({config_version}) doesn't match VERSION file ({master_version})"
            )
            print(f"   ❌ VERSION_SYNC.json needs update!")
            return False
    
    def run_tests(self) -> bool:
        """Run all version synchronization tests."""
        print("=" * 70)
        print("🧪 Media Web Viewer - Version Synchronization Test Suite")
        print("=" * 70)
        
        try:
            # Load configuration
            master_version = self.load_master_version()
            config = self.load_sync_config()
            
            # Validate version format
            version_format = config.get('version_format', {})
            if version_format:
                pattern = version_format.get('pattern', r'^\d+\.\d+\.\d+$')
                self.validate_version_format(master_version, pattern)
            
            # Check VERSION_SYNC.json consistency
            self.check_version_sync_consistency(config, master_version)
            
            # Check all sync locations
            print("\n" + "=" * 70)
            print(f"📝 Checking {len(config['sync_locations'])} sync locations...")
            print("=" * 70)
            
            all_passed = True
            for location in config['sync_locations']:
                if not self.check_location(location, master_version):
                    all_passed = False
            
            # Print summary
            print("\n" + "=" * 70)
            print("📊 Test Summary")
            print("=" * 70)
            
            if self.warnings:
                print(f"\n⚠️  Warnings ({len(self.warnings)}):")
                for warning in self.warnings:
                    print(f"   - {warning}")
            
            if self.errors:
                print(f"\n❌ Errors ({len(self.errors)}):")
                for error in self.errors:
                    print(f"   - {error}")
                print("\n💡 How to fix:")
                print("   1. Check VERSION_SYNC.json for all required locations")
                print("   2. Update each file with the correct version pattern")
                print("   3. Re-run this test to verify")
            else:
                print("\n✅ All version checks passed!")
                print(f"   Version {master_version} is synchronized across all locations.")
            
            return len(self.errors) == 0
            
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent.absolute()
    tester = VersionSyncTester(project_root)
    
    success = tester.run_tests()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ Version synchronization test PASSED")
        sys.exit(0)
    else:
        print("❌ Version synchronization test FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Environment Information Test
# Eingabewerte: Conda environments, System Python, Virtual environments, Installed packages
# Ausgabewerte: Environment discovery results, Package listings
# Testdateien: Keine (System-Informationen)
# Kommentar: Testet erweiterte Environment-Informationen (Conda, System Python, venvs, Packages).
"""
Test Suite for Extended Environment Information Display
========================================================

This module tests the extended environment information functionality including:
- Conda environments discovery
- System Python installations
- Local virtual environments
- Installed packages listing

Author: Media Web Viewer Team
Created: 2026-03-08
Version: 1.0.0
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parents[3]

from src.core.main import get_environment_info

# =============================================================================
# Test: Environment Info API Returns Required Keys
# =============================================================================

def test_environment_info_has_all_keys():
    """
    Test that get_environment_info() returns all required keys.
    
    Validates:
        - Basic environment info (python_version, executable, etc.)
        - Current environment details
        - Available Conda environments list
        - Available system Pythons list
        - Local venvs list
        - Installed packages list
    
    Raises:
        AssertionError: If any required key is missing
    """
    print("\n" + "═" * 70)
    print("TEST: Environment Info API - Required Keys")
    print("═" * 70)
    
    print("\n🔍 Calling get_environment_info()...")
    info = get_environment_info()
    
    required_keys = [
        # Basic info
        "python_version",
        "python_executable",
        "env_type",
        "env_path",
        "env_name",
        
        # Current environment details
        "current_environment",
        
        # Alternative environments
        "available_conda_environments",
        "available_system_pythons",
        "local_venvs",
        
        # Packages
        "installed_packages",
        "package_count",
        
        # Recommendations
        "recommended_environment",
    ]
    
    print(f"\n📋 Checking for required keys ({len(required_keys)}):")
    missing_keys = []
    
    for key in required_keys:
        if key in info:
            print(f"  ✓ {key}")
        else:
            print(f"  ✗ {key} - MISSING!")
            missing_keys.append(key)
    
    assert not missing_keys, f"Missing required keys: {missing_keys}"
    
    print(f"\n✅ All {len(required_keys)} required keys present")

# =============================================================================
# Test: Conda Environments Discovery
# =============================================================================

def test_conda_environments_structure():
    """
    Test that Conda environments are discovered with correct structure.
    
    Validates:
        - available_conda_environments is a list
        - Each environment has: name, path, version, recommended
        - At least one environment found (if conda is available)
    
    Raises:
        AssertionError: If structure is incorrect
    """
    print("\n" + "═" * 70)
    print("TEST: Conda Environments Discovery")
    print("═" * 70)
    
    info = get_environment_info()
    conda_envs = info.get("available_conda_environments", [])
    
    print(f"\n🐍 Found {len(conda_envs)} Conda environment(s)")
    
    assert isinstance(conda_envs, list), "available_conda_environments must be a list"
    
    if conda_envs:
        print("\n📋 Conda Environments:")
        for env in conda_envs:
            # Check structure
            assert "name" in env, "Each conda env must have 'name'"
            assert "path" in env, "Each conda env must have 'path'"
            assert "version" in env, "Each conda env must have 'version'"
            assert "recommended" in env, "Each conda env must have 'recommended'"
            
            rec_badge = "⭐" if env["recommended"] else ""
            print(f"  • {env['name']}: {env['version']} {rec_badge}")
            print(f"    Path: {env['path']}")
        
        # Check if p14 is marked as recommended
        p14_envs = [e for e in conda_envs if e["name"] == "p14"]
        if p14_envs:
            assert p14_envs[0]["recommended"], "p14 should be marked as recommended"
            print(f"\n✓ p14 correctly marked as recommended")
    else:
        print("  ℹ️  No Conda environments found (conda may not be installed)")
    
    print(f"\n✅ Conda environments structure validated")

# =============================================================================
# Test: System Python Installations
# =============================================================================

def test_system_pythons_structure():
    """
    Test that system Python installations are discovered correctly.
    
    Validates:
        - available_system_pythons is a list
        - Each Python has: path, version
        - At least one system Python found
    
    Raises:
        AssertionError: If structure is incorrect or no Pythons found
    """
    print("\n" + "═" * 70)
    print("TEST: System Python Installations")
    print("═" * 70)
    
    info = get_environment_info()
    system_pythons = info.get("available_system_pythons", [])
    
    print(f"\n🌐 Found {len(system_pythons)} system Python installation(s)")
    
    assert isinstance(system_pythons, list), "available_system_pythons must be a list"
    assert len(system_pythons) > 0, "Should find at least one system Python"
    
    print("\n📋 System Pythons:")
    for python in system_pythons:
        # Check structure
        assert "path" in python, "Each system python must have 'path'"
        assert "version" in python, "Each system python must have 'version'"
        
        print(f"  • {python['version']}")
        print(f"    Path: {python['path']}")
    
    print(f"\n✅ System Python installations validated")

# =============================================================================
# Test: Local Virtual Environments
# =============================================================================

def test_local_venvs_structure():
    """
    Test that local virtual environments are discovered correctly.
    
    Validates:
        - local_venvs is a list
        - Each venv has: name, path, version, is_current
        - Current venv is correctly identified
    
    Raises:
        AssertionError: If structure is incorrect
    """
    print("\n" + "═" * 70)
    print("TEST: Local Virtual Environments")
    print("═" * 70)
    
    info = get_environment_info()
    local_venvs = info.get("local_venvs", [])
    
    print(f"\n📁 Found {len(local_venvs)} local virtual environment(s)")
    
    assert isinstance(local_venvs, list), "local_venvs must be a list"
    
    if local_venvs:
        print("\n📋 Local Venvs:")
        current_count = 0
        
        for venv in local_venvs:
            # Check structure
            assert "name" in venv, "Each venv must have 'name'"
            assert "path" in venv, "Each venv must have 'path'"
            assert "version" in venv, "Each venv must have 'version'"
            assert "is_current" in venv, "Each venv must have 'is_current'"
            
            current_badge = "● AKTIV" if venv["is_current"] else ""
            print(f"  • {venv['name']}: {venv['version']} {current_badge}")
            print(f"    Path: {venv['path']}")
            
            if venv["is_current"]:
                current_count += 1
        
        # Should have at most one current venv
        assert current_count <= 1, "Only one venv can be current"
        
        if current_count == 1:
            print(f"\n✓ Current venv correctly identified")
    else:
        print("  ℹ️  No local virtual environments found in project directory")
    
    print(f"\n✅ Local venvs structure validated")

# =============================================================================
# Test: Installed Packages
# =============================================================================

def test_installed_packages_structure():
    """
    Test that installed packages are listed correctly.
    
    Validates:
        - installed_packages is a list
        - package_count matches list length
        - Each package has: name, version
        - Critical packages are present (eel, mutagen, bottle)
    
    Raises:
        AssertionError: If structure is incorrect or critical packages missing
    """
    print("\n" + "═" * 70)
    print("TEST: Installed Packages")
    print("═" * 70)
    
    info = get_environment_info()
    packages = info.get("installed_packages", [])
    package_count = info.get("package_count", 0)
    
    print(f"\n📦 Found {len(packages)} installed package(s)")
    
    assert isinstance(packages, list), "installed_packages must be a list"
    assert package_count == len(packages), "package_count must match list length"
    assert len(packages) > 0, "Should have at least some packages installed"
    
    # Check structure of first few packages
    print("\n📋 Sample packages:")
    for pkg in packages[:5]:
        assert "name" in pkg, "Each package must have 'name'"
        assert "version" in pkg, "Each package must have 'version'"
        print(f"  • {pkg['name']}: {pkg['version']}")
    
    if len(packages) > 5:
        print(f"  ... and {len(packages) - 5} more")
    
    # Check for critical packages
    print("\n🔍 Checking critical packages:")
    package_names = {pkg["name"].lower() for pkg in packages}
    
    critical_packages = ["eel", "mutagen", "bottle"]
    for pkg_name in critical_packages:
        if pkg_name in package_names:
            # Find version
            pkg_info = next(p for p in packages if p["name"].lower() == pkg_name)
            print(f"  ✓ {pkg_name}: {pkg_info['version']}")
            assert True
        else:
            print(f"  ✗ {pkg_name}: NOT FOUND")
            pytest.fail(f"Critical package missing: {pkg_name}")
    
    print(f"\n✅ Installed packages validated ({package_count} total)")

# =============================================================================
# Test: Current Environment Identification
# =============================================================================

def test_current_environment_correct():
    """
    Test that the current environment is correctly identified.
    
    Validates:
        - current_environment has correct structure
        - Environment type is set (conda/venv/system)
        - Python version matches sys.version_info
    
    Raises:
        AssertionError: If current environment info is incorrect
    """
    print("\n" + "═" * 70)
    print("TEST: Current Environment Identification")
    print("═" * 70)
    
    info = get_environment_info()
    current_env = info.get("current_environment", {})
    
    print("\n🔍 Current Environment:")
    
    assert isinstance(current_env, dict), "current_environment must be a dict"
    
    required_fields = ["type", "name", "path", "python_version", "python_executable"]
    for field in required_fields:
        assert field in current_env, f"current_environment must have '{field}'"
    
    print(f"  • Type: {current_env['type']}")
    print(f"  • Name: {current_env['name']}")
    print(f"  • Path: {current_env['path']}")
    print(f"  • Python Version: {current_env['python_version']}")
    print(f"  • Executable: {current_env['python_executable']}")
    
    # Validate environment type
    assert current_env["type"] in ["conda", "venv", "system"], \
        f"Invalid environment type: {current_env['type']}"
    
    # Validate Python version matches
    import platform
    expected_version = platform.python_version()
    assert current_env["python_version"] == expected_version, \
        f"Python version mismatch: {current_env['python_version']} vs {expected_version}"
    
    # Validate executable matches
    assert current_env["python_executable"] == sys.executable, \
        "Python executable mismatch"
    
    print(f"\n✅ Current environment correctly identified")

# =============================================================================
# Test: JSON Serialization
# =============================================================================

def test_environment_info_json_serializable():
    """
    Test that the entire environment info dict is JSON serializable.
    
    This is important for the Eel API which needs to serialize
    the response to send to the frontend.
    
    Validates:
        - Info dict can be serialized to JSON
        - Deserialized data matches original structure
    
    Raises:
        AssertionError: If JSON serialization fails
    """
    print("\n" + "═" * 70)
    print("TEST: JSON Serialization")
    print("═" * 70)
    
    print("\n🔍 Testing JSON serialization...")
    
    info = get_environment_info()
    
    try:
        # Serialize to JSON
        json_str = json.dumps(info, indent=2)
        print(f"  ✓ Serialization successful ({len(json_str)} bytes)")
        
        # Deserialize
        deserialized = json.loads(json_str)
        print(f"  ✓ Deserialization successful")
        
        # Check key preservation
        assert set(deserialized.keys()) == set(info.keys()), \
            "Keys changed during serialization"
        print(f"  ✓ All {len(info.keys())} keys preserved")
        
        # Show sample of JSON output
        print(f"\n📄 JSON Preview (first 500 chars):")
        print("─" * 70)
        print(json_str[:500] + "..." if len(json_str) > 500 else json_str)
        print("─" * 70)
        
    except (TypeError, ValueError) as e:
        pytest.fail(f"JSON serialization failed: {e}")
    
    print(f"\n✅ Environment info is JSON serializable")

# =============================================================================
# Main Test Execution
# =============================================================================

if __name__ == "__main__":
    """
    Run all environment info tests when script is executed directly.
    
    Usage:
        python test_environment_info.py
        pytest test_environment_info.py -v -s
    """
    print("\n" + "═" * 70)
    print("  EXTENDED ENVIRONMENT INFORMATION - TEST SUITE")
    print("═" * 70)
    
    # Run all tests
    pytest.main([__file__, "-v", "-s"])

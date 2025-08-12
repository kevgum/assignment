#!/usr/bin/env python3
"""
Simplified build script for Hotel Booking System
This script runs the complete CI/CD pipeline without requiring Maven
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description, allow_failure=False):
    """Run a command and handle errors"""
    print(f"\n[BUILD] {description}...")
    
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        print(f"✓ {description} completed successfully")
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        
        if not allow_failure:
            return False
        else:
            print("WARNING: Continuing despite failure...")
            return True


def main():
    """Main build process"""
    print("=" * 60)
    print("Hotel Booking System - CI/CD Pipeline")
    print("=" * 60)
    
    # Create target directories
    os.makedirs("target/surefire-reports", exist_ok=True)
    os.makedirs("target/dist", exist_ok=True)
    
    # Build phases
    phases = [
        ("python3 --version", "Checking Python version"),
        ("pip3 install --user -r requirements.txt", "Installing dependencies"),
        ("python3 -m py_compile hotel.py", "Compiling Python code"),
        ("python3 -m pytest tests/ -v --tb=short --junitxml=target/surefire-reports/pytest-results.xml", "Running unit tests"),
        ("python3 setup.py sdist --dist-dir target/dist", "Creating distribution package"),
    ]
    
    for command, description in phases:
        success = run_command(command, description)
        if not success:
            print(f"ERROR: {description} failed")
            return 1
    
    # Additional packaging
    print("\n[BUILD] Creating deployment artifacts...")
    
    # Copy main files to deployment directory
    deployment_dir = "target/deployment"
    os.makedirs(deployment_dir, exist_ok=True)
    
    files_to_copy = ["hotel.py", "requirements.txt", "README.md"]
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, deployment_dir)
            print(f"✓ Copied {file} to deployment directory")
    
    # Test the application
    print("\n[BUILD] Testing application functionality...")
    test_command = "python3 hotel.py single 2"
    run_command(test_command, "Testing hotel booking functionality", allow_failure=True)
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("✓ Build artifacts in 'target/' directory")
    print("✓ Test reports in 'target/surefire-reports/'")
    print("✓ Distribution packages in 'target/dist/'")
    print("✓ Deployment files in 'target/deployment/'")
    print("\nUsage: python3 hotel.py [room_type] [days]")
    print("Example: python3 hotel.py luxury 2")
    
    return 0


if __name__ == "__main__":
    exit(main())

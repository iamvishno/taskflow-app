#!/usr/bin/env python3
"""
Setup verification script for AI Chatbot
Checks if all requirements are met before running the application
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"[X] Python 3.8+ required. You have {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"[OK] Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'anthropic',
        'dotenv',
        'pydantic'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package if package != 'dotenv' else 'dotenv')
            print(f"[OK] {package} installed")
        except ImportError:
            print(f"[X] {package} not installed")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n[!] Missing packages. Run: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has API key"""
    env_file = Path('.env')

    if not env_file.exists():
        print("[X] .env file not found")
        print("    Create one by copying .env.example:")
        print("    Windows: copy .env.example .env")
        print("    Mac/Linux: cp .env.example .env")
        return False

    print("[OK] .env file exists")

    # Check if API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if 'your_api_key_here' in content:
            print("[!] API key not set in .env file")
            print("    Get your key from: https://console.anthropic.com/")
            print("    Then update ANTHROPIC_API_KEY in .env file")
            return False
        elif 'ANTHROPIC_API_KEY=' in content:
            print("[OK] API key appears to be set")
            return True

    return False

def check_static_files():
    """Check if static files exist"""
    static_dir = Path('static')
    required_files = ['index.html', 'styles.css', 'app.js']

    if not static_dir.exists():
        print("[X] static/ directory not found")
        return False

    print("[OK] static/ directory exists")

    for file in required_files:
        file_path = static_dir / file
        if not file_path.exists():
            print(f"[X] {file} not found in static/")
            return False
        print(f"[OK] {file} exists")

    return True

def main():
    """Run all checks"""
    print("=" * 60)
    print("AI Chatbot - Setup Verification")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Static Files", check_static_files),
    ]

    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        print("-" * 60)
        result = check_func()
        results.append(result)
        print()

    print("=" * 60)
    if all(results):
        print("[OK] All checks passed! You're ready to run the application.")
        print("\nTo start the server, run:")
        print("  python main.py")
        print("\nThen open your browser to: http://localhost:8000")
        return 0
    else:
        print("[X] Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

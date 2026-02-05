#!/usr/bin/env python3
"""
Verification script to check that all files are present and properly structured.

Run this to verify the installation is complete before running the formatter.
"""

import os
import sys
from pathlib import Path

# Configure stdout for UTF-8 on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def check_file_exists(filepath, description):
    """Check if a file exists and report."""
    if filepath.exists():
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ {description} - MISSING: {filepath}")
        return False


def verify_structure():
    """Verify all required files and directories exist."""
    print("Verifying Puzzle Results Formatter structure...")
    print("=" * 60)

    base_dir = Path(__file__).parent
    all_good = True

    # Check main files
    print("\nMain Files:")
    all_good &= check_file_exists(base_dir / "formatter.py", "Main formatter script")
    all_good &= check_file_exists(base_dir / "config.json", "Configuration file")
    all_good &= check_file_exists(base_dir / "requirements.txt", "Requirements file")
    all_good &= check_file_exists(base_dir / "README.md", "README documentation")

    # Check puzzle_formatters directory
    print("\nPuzzle Formatters:")
    formatters_dir = base_dir / "puzzle_formatters"
    all_good &= check_file_exists(formatters_dir / "__init__.py", "Formatter registry")
    all_good &= check_file_exists(formatters_dir / "base.py", "Base formatter class")
    all_good &= check_file_exists(formatters_dir / "framed.py", "Framed formatter")
    all_good &= check_file_exists(formatters_dir / "quolture.py", "Quolture formatter")
    all_good &= check_file_exists(formatters_dir / "wordle.py", "Wordle formatter")

    # Check documentation
    print("\nDocumentation:")
    docs_dir = base_dir / "docs"
    all_good &= check_file_exists(docs_dir / "ARCHITECTURE.md", "Architecture docs")
    all_good &= check_file_exists(docs_dir / "ADDING_PUZZLES.md", "Adding puzzles guide")
    all_good &= check_file_exists(docs_dir / "EXAMPLES.md", "Examples documentation")

    # Check tests
    print("\nTests:")
    tests_dir = base_dir / "tests"
    all_good &= check_file_exists(tests_dir / "test_formatter.py", "Test suite")

    # Try importing modules
    print("\nModule Imports:")
    try:
        sys.path.insert(0, str(base_dir))
        from puzzle_formatters import (
            BasePuzzleFormatter,
            FramedFormatter,
            FramedOneFrameFormatter,
            QuoltureFormatter,
            WordleFormatter,
            ALL_FORMATTERS,
        )
        print(f"  ✓ Successfully imported all formatters")
        print(f"  ✓ Found {len(ALL_FORMATTERS)} registered formatters")
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        all_good = False

    # Check config
    print("\nConfiguration:")
    try:
        import json
        config_path = base_dir / "config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if 'puzzle_order' in config:
            print(f"  ✓ Config has puzzle_order")
            print(f"    Order: {', '.join(config['puzzle_order'])}")
        else:
            print(f"  ✗ Config missing puzzle_order")
            all_good = False
    except Exception as e:
        print(f"  ✗ Config error: {e}")
        all_good = False

    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("✓ All checks passed! Structure is complete.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run tests: python tests/test_formatter.py")
        print("  3. Try formatter: python formatter.py --help")
        return 0
    else:
        print("✗ Some checks failed. Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(verify_structure())

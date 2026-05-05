#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

"""
Verification script to check that all files are present and properly structured.

Run this to verify the installation is complete before running the formatter.
"""

import io
import os
import sys

# Configure stdout for UTF-8 on Windows
if sys.platform == 'win32':
    if sys.version_info[0] >= 3:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    else:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout, errors='replace')


def check_file_exists(filepath, description):
    """Check if a file exists and report."""
    if os.path.exists(filepath):
        print("  ✓ {}".format(description))
        return True
    else:
        print("  ✗ {} - MISSING: {}".format(description, filepath))
        return False


def verify_structure():
    """Verify all required files and directories exist."""
    print("Verifying Puzzle Results Formatter structure...")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_good = True

    # Check main files
    print("\nMain Files:")
    all_good &= check_file_exists(os.path.join(base_dir, "formatter.py"), "Main formatter script")
    all_good &= check_file_exists(os.path.join(base_dir, "config.json"), "Configuration file")
    all_good &= check_file_exists(os.path.join(base_dir, "requirements.txt"), "Requirements file")
    all_good &= check_file_exists(os.path.join(base_dir, "README.md"), "README documentation")

    # Check puzzle_formatters directory
    print("\nPuzzle Formatters:")
    formatters_dir = os.path.join(base_dir, "puzzle_formatters")
    all_good &= check_file_exists(os.path.join(formatters_dir, "__init__.py"), "Formatter registry")
    all_good &= check_file_exists(os.path.join(formatters_dir, "base.py"), "Base formatter class")
    all_good &= check_file_exists(os.path.join(formatters_dir, "framed.py"), "Framed formatter")
    all_good &= check_file_exists(os.path.join(formatters_dir, "quolture.py"), "Quolture formatter")
    all_good &= check_file_exists(os.path.join(formatters_dir, "wordle.py"), "Wordle formatter")

    # Check documentation
    print("\nDocumentation:")
    docs_dir = os.path.join(base_dir, "docs")
    all_good &= check_file_exists(os.path.join(docs_dir, "ARCHITECTURE.md"), "Architecture docs")
    all_good &= check_file_exists(os.path.join(docs_dir, "ADDING_PUZZLES.md"), "Adding puzzles guide")
    all_good &= check_file_exists(os.path.join(docs_dir, "EXAMPLES.md"), "Examples documentation")

    # Check tests
    print("\nTests:")
    tests_dir = os.path.join(base_dir, "tests")
    all_good &= check_file_exists(os.path.join(tests_dir, "test_formatter.py"), "Test suite")

    # Try importing modules
    print("\nModule Imports:")
    try:
        sys.path.insert(0, base_dir)
        from puzzle_formatters import (
            BasePuzzleFormatter,
            FramedFormatter,
            FramedOneFrameFormatter,
            QuoltureFormatter,
            WordleFormatter,
            ALL_FORMATTERS,
        )
        print("  ✓ Successfully imported all formatters")
        print("  ✓ Found {} registered formatters".format(len(ALL_FORMATTERS)))
    except ImportError as e:
        print("  ✗ Import error: {}".format(e))
        all_good = False

    # Check config
    print("\nConfiguration:")
    try:
        import json
        config_path = os.path.join(base_dir, "config.json")
        with io.open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if 'puzzle_order' in config:
            print("  ✓ Config has puzzle_order")
            print("    Order: {}".format(', '.join(config['puzzle_order'])))
        else:
            print("  ✗ Config missing puzzle_order")
            all_good = False
    except Exception as e:
        print("  ✗ Config error: {}".format(e))
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

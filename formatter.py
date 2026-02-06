#!/usr/bin/env python3
"""
Puzzle Results Formatter

Collates and formats daily puzzle results (Wordle, Framed, Quolture, etc.)
into a standardized format for sharing in Teams chat.

Usage:
    python formatter.py

Features:
    - Interactive mode: paste puzzle results as you complete them
    - Auto-detects puzzle completion
    - Auto-copies formatted results to clipboard
    - Supports multiple puzzles in any order

Author: Created for daily puzzle result sharing 
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Configure stdout for UTF-8 on Windows to handle emoji properly
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip not installed. Run: pip install pyperclip")
    sys.exit(1)

from puzzle_formatters import get_formatter_for_text


def load_config() -> dict:
    """
    Load configuration from config.json.

    Returns:
        Dictionary containing puzzle_order list

    Raises:
        SystemExit if config.json not found or invalid
    """
    config_path = Path(__file__).parent / "config.json"

    if not config_path.exists():
        print(f"Error: config.json not found at {config_path}")
        sys.exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config.json: {e}")
        sys.exit(1)


def split_into_puzzle_blocks(text: str) -> List[str]:
    """
    Split input text into individual puzzle blocks.

    Puzzle blocks are separated by URLs and known puzzle headers.
    This allows handling puzzles pasted in any order, including puzzles without URLs.

    Args:
        text: Raw input containing one or more puzzle results

    Returns:
        List of text blocks, each potentially containing one puzzle
    """
    # Split before known puzzle headers
    # Pattern: Match start of known puzzle titles at beginning of line
    puzzle_headers = [
        r'(?=^Framed\s)',
        r'(?=^Wordle\s)',
        r'(?=^Connections\s*\n)',
        r'(?=^"Quolture")',
        r'(?=^Strands\s)',
    ]

    text_with_delimiters = text
    for pattern in puzzle_headers:
        text_with_delimiters = re.sub(pattern, '---PUZZLE_BREAK---', text_with_delimiters, flags=re.MULTILINE)

    # Also split by URLs (remove URLs and create breaks)
    url_pattern = r'https?://[^\s]+'
    text_with_delimiters = re.sub(url_pattern, '\n---PUZZLE_BREAK---\n', text_with_delimiters)

    # Split by the delimiter
    blocks = text_with_delimiters.split('---PUZZLE_BREAK---')

    # Clean up blocks: remove empty ones and strip whitespace
    blocks = [block.strip() for block in blocks if block.strip()]

    return blocks


def detect_and_parse_puzzles(text: str) -> List[Dict]:
    """
    Detect all puzzles in the input text and parse them.

    Args:
        text: Raw input containing puzzle results

    Returns:
        List of dictionaries, each containing:
            - 'formatter': The formatter instance that handles this puzzle
            - 'data': Parsed puzzle data
            - 'puzzle_name': Identifier for sorting (e.g., "wordle")
    """
    blocks = split_into_puzzle_blocks(text)
    detected_puzzles = []

    for block in blocks:
        # Try to find a formatter that can handle this block
        formatter = get_formatter_for_text(block)

        if formatter:
            # Parse the puzzle data
            puzzle_data = formatter.parse(block)

            if puzzle_data:
                detected_puzzles.append({
                    'formatter': formatter,
                    'data': puzzle_data,
                    'puzzle_name': formatter.puzzle_name
                })

    return detected_puzzles


def sort_puzzles_by_config(puzzles: List[Dict], puzzle_order: List[str]) -> List[Dict]:
    """
    Sort detected puzzles according to the configured order.

    Puzzles not in the config are placed at the end in order of detection.

    Args:
        puzzles: List of detected puzzle dictionaries
        puzzle_order: Ordered list of puzzle_name identifiers from config

    Returns:
        Sorted list of puzzle dictionaries
    """
    def get_sort_key(puzzle):
        """
        Generate sort key for a puzzle.

        Returns tuple (priority, original_index) where:
        - priority: Lower numbers come first (position in config, or 9999 if not in config)
        - original_index: Maintains detection order for puzzles not in config
        """
        puzzle_name = puzzle['puzzle_name']
        try:
            # Get position in configured order (0-based)
            priority = puzzle_order.index(puzzle_name)
        except ValueError:
            # Not in config - put at end
            priority = 9999

        return priority

    return sorted(puzzles, key=get_sort_key)


def format_output(puzzles: List[Dict]) -> str:
    """
    Format all puzzles into final output string.

    Applies formatting rules:
    - Single-line puzzles (Framed, Quolture) have no blank lines between them
    - Wordle (multi-line) is separated by a blank line from previous puzzles

    Args:
        puzzles: Sorted list of puzzle dictionaries

    Returns:
        Formatted string ready for sharing
    """
    if not puzzles:
        return ""

    formatted_parts = []
    previous_was_multiline = False

    for puzzle in puzzles:
        formatter = puzzle['formatter']
        data = puzzle['data']

        # Format this puzzle
        formatted = formatter.format(data)

        # Determine if this is a multi-line puzzle (Wordle)
        is_multiline = '\n' in formatted

        # Add blank line before Wordle if there were previous puzzles
        if is_multiline and formatted_parts:
            formatted_parts.append('')  # Blank line separator

        formatted_parts.append(formatted)
        previous_was_multiline = is_multiline

    return '\n'.join(formatted_parts)


def process_puzzle_results(input_text: str) -> str:
    """
    Main processing function: parse, sort, and format puzzle results.

    Args:
        input_text: Raw puzzle results (can be in any order)

    Returns:
        Formatted puzzle results ready for sharing
    """
    # Load configuration
    config = load_config()
    puzzle_order = config.get('puzzle_order', [])

    # Detect and parse all puzzles
    puzzles = detect_and_parse_puzzles(input_text)

    if not puzzles:
        return "No recognized puzzles found in input."

    # Sort puzzles by configured order
    sorted_puzzles = sort_puzzles_by_config(puzzles, puzzle_order)

    # Format into final output
    output = format_output(sorted_puzzles)

    return output


def interactive_mode():
    """
    Interactive mode: Read puzzles from clipboard one at a time.

    User workflow:
    1. Complete a puzzle and copy the result (Ctrl+C)
    2. Press Enter in this terminal to capture it
    3. Repeat for more puzzles throughout the day
    4. Press Ctrl+C when done to format all puzzles
    """
    print("=== Puzzle Results Formatter ===")
    print("1. Complete a puzzle and copy the result (Ctrl+C)")
    print("2. Press Enter here to capture it")
    print("3. Repeat for more puzzles")
    print("4. Press Ctrl+C when done with all puzzles")
    print()

    all_puzzles_text = []

    try:
        while True:
            # Wait for Enter keypress
            input("Press Enter to read from clipboard (or Ctrl+C when done): ")

            # Read entire clipboard content
            clipboard_content = pyperclip.paste()

            # Check if clipboard is empty
            if not clipboard_content.strip():
                print("  ⚠ Clipboard is empty - copy a puzzle result first")
                print()
                continue

            # Try to identify what puzzle this is
            formatter = get_formatter_for_text(clipboard_content)

            if formatter:
                print(f"  ✓ Captured {formatter.puzzle_name.replace('_', ' ').title()}")
                all_puzzles_text.append(clipboard_content)
            else:
                print("  ⚠ Unrecognized puzzle format (will try to process anyway)")
                all_puzzles_text.append(clipboard_content)

            print()

    except (EOFError, KeyboardInterrupt):
        print("\n")

        if not all_puzzles_text:
            print("No puzzles captured. Exiting.")
            return

        # Process all captured puzzles
        # Join with double newline to separate puzzles
        combined_input = '\n\n'.join(all_puzzles_text)
        output = process_puzzle_results(combined_input)

        print("=== Formatted Results ===")
        print(output)
        print()

        # Copy result to clipboard
        try:
            pyperclip.copy(output)
            print("✓ Results copied to clipboard!")
        except Exception as e:
            print(f"Note: Could not copy to clipboard: {e}")

        print("\nPaste into Teams and share your results!")
        input("Press Enter to exit.")


def main():
    """
    Main entry point: Run interactive mode with auto-copy to clipboard.
    """
    interactive_mode()


if __name__ == '__main__':
    main()

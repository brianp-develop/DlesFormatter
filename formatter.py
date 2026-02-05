#!/usr/bin/env python3
"""
Puzzle Results Formatter

Collates and formats daily puzzle results (Wordle, Framed, Quolture, etc.)
into a standardized format for sharing in Teams chat.

Usage:
    # Interactive mode (default) - paste multiple times, keeps running
    python formatter.py

    # Clipboard mode - one-shot processing
    python formatter.py --clipboard
    python formatter.py -c

Author: Created for daily puzzle result sharing
"""

import argparse
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

    Puzzle blocks are separated by URLs or double line breaks.
    This allows handling puzzles pasted in any order.

    Args:
        text: Raw input containing one or more puzzle results

    Returns:
        List of text blocks, each potentially containing one puzzle
    """
    # First, split by URLs (each puzzle typically ends with a URL)
    # Pattern matches http/https URLs
    url_pattern = r'https?://[^\s]+'

    # Replace URLs with a special delimiter
    text_with_delimiters = re.sub(url_pattern, '\n---PUZZLE_BREAK---\n', text)

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
    Interactive mode: Accept multiple pastes, keep running until user exits.

    User can paste puzzle results multiple times as they complete them.
    Press Enter on empty input or Ctrl+C to process and exit.
    """
    print("=== Puzzle Results Formatter (Interactive Mode) ===")
    print("Paste your puzzle results below.")
    print("You can paste multiple times as you complete puzzles.")
    print("Press Enter on empty input when done, or Ctrl+C to exit.")
    print()

    all_input_lines = []

    try:
        while True:
            print("Paste puzzle results (or press Enter if done):")
            lines = []

            # Read lines until we get an empty line or EOF
            while True:
                try:
                    line = input()
                    if not line.strip() and not lines:
                        # Empty input on first line = user is done
                        if all_input_lines:
                            # Process what we have
                            raise EOFError()
                        else:
                            # No input yet, continue waiting
                            continue
                    lines.append(line)

                    # Check if this looks like end of a puzzle (blank line after content)
                    if not line.strip() and lines:
                        # End of this paste
                        break
                except EOFError:
                    # Ctrl+D or end of input
                    raise

            if lines:
                all_input_lines.extend(lines)
                print(f"  -> Captured {len(lines)} lines")
                print()

    except (EOFError, KeyboardInterrupt):
        print("\n")

        if not all_input_lines:
            print("No input received. Exiting.")
            return

        # Process all accumulated input
        input_text = '\n'.join(all_input_lines)
        output = process_puzzle_results(input_text)

        print("=== Formatted Results ===")
        print(output)
        print()

        # Copy to clipboard
        try:
            pyperclip.copy(output)
            print("✓ Results copied to clipboard!")
        except Exception as e:
            print(f"Note: Could not copy to clipboard: {e}")

        print("\nPaste into Teams and share your results!")


def clipboard_mode():
    """
    Clipboard mode: Read from clipboard, format, copy back to clipboard.

    One-shot processing for quick daily use.
    """
    print("=== Puzzle Results Formatter (Clipboard Mode) ===")

    # Read from clipboard
    try:
        input_text = pyperclip.paste()
    except Exception as e:
        print(f"Error: Could not read from clipboard: {e}")
        sys.exit(1)

    if not input_text.strip():
        print("Error: Clipboard is empty")
        sys.exit(1)

    print("Processing puzzle results from clipboard...")

    # Process the input
    output = process_puzzle_results(input_text)

    # Display result
    print("\n=== Formatted Results ===")
    print(output)
    print()

    # Copy back to clipboard
    try:
        pyperclip.copy(output)
        print("✓ Results copied to clipboard!")
    except Exception as e:
        print(f"Note: Could not copy to clipboard: {e}")

    print("\nPaste into Teams and share your results!")


def main():
    """
    Main entry point: Parse arguments and run appropriate mode.
    """
    parser = argparse.ArgumentParser(
        description="Format daily puzzle results for sharing in Teams chat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default) - paste as you go
  python formatter.py

  # Clipboard mode - one-shot processing
  python formatter.py --clipboard
  python formatter.py -c

Supported Puzzles:
  - Framed
  - Framed One Frame Challenge
  - Quolture
  - Wordle
        """
    )

    parser.add_argument(
        '-c', '--clipboard',
        action='store_true',
        help='Clipboard mode: read from clipboard, format, copy back'
    )

    args = parser.parse_args()

    if args.clipboard:
        clipboard_mode()
    else:
        interactive_mode()


if __name__ == '__main__':
    main()

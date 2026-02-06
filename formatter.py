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


def _is_wordle_complete(lines: List[str]) -> bool:
    """
    Check if a Wordle puzzle is complete (6 emoji rows = max attempts used).

    Wordle allows a maximum of 6 guesses. If the user pastes 6 rows of emoji
    squares (🟩🟨⬛⬜), the puzzle is complete even without an all-green row,
    meaning they failed to solve it within the attempt limit.

    This complements the end_marker_pattern check (which detects all-green rows)
    to handle both successful solves and failed attempts.

    Args:
        lines: List of input lines accumulated so far

    Returns:
        True if 6 or more Wordle emoji rows are present
    """
    wordle_emoji_pattern = r'^[🟩🟨⬛⬜]{5}$'
    emoji_rows = [line for line in lines if re.match(wordle_emoji_pattern, line.strip())]
    return len(emoji_rows) >= 6


def _is_connections_complete(lines: List[str]) -> bool:
    """
    Check if a Connections puzzle is complete using solid/mixed row logic.

    Connections puzzles involve grouping 16 words into 4 categories. Each correct
    category shows as a row of 4 same-colored emojis (solid row). Wrong attempts
    show mixed colors (mixed row).

    Game completion rules:
    - Solved successfully: 4 solid rows (perfect categories) + 0-3 mixed rows (mistakes)
    - Failed to solve: 4+ mixed rows (too many mistakes) + 0-2 solid rows

    This detection cannot use a simple end_marker_pattern because there's no URL
    and completion depends on counting row types, not matching a single pattern.

    Args:
        lines: List of input lines accumulated so far

    Returns:
        True if puzzle shows completion pattern (4 solid or 4 mixed rows)
    """
    connections_emoji_pattern = r'^[🟦🟪🟩🟨]{4}$'
    connections_rows = [line for line in lines if re.match(connections_emoji_pattern, line.strip())]

    if len(connections_rows) < 4:
        return False

    # Count solid rows (all 4 emojis same color = correct category)
    # Count mixed rows (different colors = wrong attempt)
    solid_rows = 0
    mixed_rows = 0

    for row in connections_rows:
        emojis = list(row.strip())
        if len(set(emojis)) == 1:  # All same emoji = solid row
            solid_rows += 1
        else:
            mixed_rows += 1

    # Complete if: 4 solid + (0-3 mixed), OR 4 mixed + (0-2 solid)
    return (solid_rows >= 4 and mixed_rows <= 3) or (mixed_rows >= 4 and solid_rows <= 2)


def check_puzzle_complete(lines: List[str]) -> bool:
    """
    Check if accumulated lines contain a complete puzzle.

    Detection strategies:
    1. Generic URL-based: Most puzzles end with a URL (Framed, Quolture)
    2. Pattern-based: Some use special markers (Wordle all-green row)
    3. Special cases: Complex logic for puzzles without clear end markers

    Args:
        lines: List of input lines accumulated so far

    Returns:
        True if puzzle completion is detected
    """
    from puzzle_formatters import ALL_FORMATTERS

    # Check generic end_marker_patterns (URLs, all-green Wordle row)
    # This handles: Framed, Framed One Frame, Quolture, and solved Wordle
    for line in lines:
        for formatter in ALL_FORMATTERS:
            if formatter.end_marker_pattern and re.search(formatter.end_marker_pattern, line):
                return True

    # Check Wordle special case: 6 attempts used (failed to solve)
    # Needed because unsolved Wordle has no all-green row to match
    if _is_wordle_complete(lines):
        return True

    # Check Connections special case: solid/mixed row counting logic
    # Needed because completion depends on row type analysis, not a single pattern
    if _is_connections_complete(lines):
        return True

    return False


def interactive_mode():
    """
    Interactive mode: Accept multiple pastes, keep running until user exits.

    User can paste puzzle results multiple times as they complete them.
    Press Enter on empty input or Ctrl+C to process and exit.
    """
    print("=== Puzzle Results Formatter (Interactive Mode) ===")
    print("Paste your puzzle results below.")
    print("The script will detect when each puzzle is complete.")
    print("Press Ctrl+C when all puzzles are entered.")
    print()

    all_input_lines = []

    try:
        while True:
            print("Paste puzzle results (or press Enter if done):")
            lines = []

            # Read lines until we detect a complete puzzle or user signals done
            while True:
                try:
                    line = input()

                    # First line empty = user signaling done
                    if not line.strip() and not lines:
                        if all_input_lines:
                            raise EOFError()
                        else:
                            continue

                    # Add line (preserve blank lines for formatting)
                    lines.append(line)

                    # Check if we just received a puzzle end marker
                    if check_puzzle_complete(lines):
                        # Found end marker, this paste is complete
                        print(f"  -> Captured {len(lines)} lines")
                        break

                    # Blank line without end marker = mid-puzzle, continue
                    # (This preserves blank lines in puzzles like Framed)

                except EOFError:
                    raise

            if lines:
                all_input_lines.extend(lines)
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
        input("Press Enter to exit.")


def main():
    """
    Main entry point: Run interactive mode with auto-copy to clipboard.
    """
    interactive_mode()


if __name__ == '__main__':
    main()

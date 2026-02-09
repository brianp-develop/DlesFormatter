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

# Constants
PUZZLE_SEPARATOR = '{PUZZLE_SEPARATOR}'
UNKNOWN_PUZZLE_PRIORITY = 9999
PIPS_DIFFICULTY_ORDER = {'Easy': 1, 'Medium': 2, 'Hard': 3}


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
        r'(?=^Pips\s)',
        r'(?=^#waffle\d+)',
    ]

    text_with_delimiters = text
    for pattern in puzzle_headers:
        text_with_delimiters = re.sub(pattern, PUZZLE_SEPARATOR, text_with_delimiters, flags=re.MULTILINE)

    # Also split by URLs (remove URLs and create breaks)
    url_pattern = r'https?://[^\s]+'
    text_with_delimiters = re.sub(url_pattern, f'\n{PUZZLE_SEPARATOR}\n', text_with_delimiters)

    # Split by the delimiter
    blocks = text_with_delimiters.split(PUZZLE_SEPARATOR)

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
    def get_sort_key(puzzle: Dict) -> int:
        """
        Generate sort key for a puzzle.

        Returns:
            Priority value - lower numbers come first (position in config, or UNKNOWN_PUZZLE_PRIORITY if not in config)
        """
        puzzle_name = puzzle['puzzle_name']
        try:
            # Get position in configured order (0-based)
            priority = puzzle_order.index(puzzle_name)
        except ValueError:
            # Not in config - put at end
            priority = UNKNOWN_PUZZLE_PRIORITY

        return priority

    return sorted(puzzles, key=get_sort_key)


def _get_puzzle_identity(puzzle: Dict) -> tuple:
    """
    Extract unique identity for a puzzle to detect duplicates.

    Different puzzle types have different identity criteria:
    - Pips: (name, number, difficulty) - Easy vs Medium are different puzzles
    - Most others: (name, number) - e.g., Wordle 1692

    Args:
        puzzle: Puzzle dictionary with 'puzzle_name' and 'data' keys

    Returns:
        Tuple representing unique identity of this puzzle
    """
    puzzle_name = puzzle['puzzle_name']
    data = puzzle['data']

    if puzzle_name == 'pips':
        # Pips: Same puzzle number but different difficulties are different puzzles
        return (puzzle_name, data['puzzle_number'], data['difficulty'])

    elif puzzle_name == 'wordle':
        # Extract puzzle number from title: "Wordle 1,692 4/6" -> "1692"
        match = re.search(r'Wordle\s+([\d,]+)', data['title'])
        if match:
            puzzle_number = match.group(1).replace(',', '')
            return (puzzle_name, puzzle_number)
        # Fallback to hash if we can't extract number
        return (puzzle_name, hash(data.get('raw_text', '')))

    elif puzzle_name in ['framed', 'framed_one_frame']:
        # Extract from data (should have puzzle_number from parsing)
        # Fallback: extract from raw_text if needed
        if 'puzzle_number' in data:
            return (puzzle_name, data['puzzle_number'])
        # Extract from raw text: "Framed #XXX" or similar
        match = re.search(r'#(\d+)', data.get('raw_text', ''))
        if match:
            return (puzzle_name, match.group(1))
        return (puzzle_name, hash(data.get('raw_text', '')))

    elif puzzle_name == 'connections':
        # Direct access to puzzle_number
        return (puzzle_name, data.get('puzzle_number', ''))

    elif puzzle_name == 'strands':
        # Direct access to puzzle_number
        return (puzzle_name, data.get('puzzle_number', ''))

    elif puzzle_name == 'waffle':
        # Direct access to puzzle_number
        return (puzzle_name, data.get('puzzle_number', ''))

    elif puzzle_name == 'quolture':
        # Extract from first line: '"Quolture" 1692'
        if data.get('lines'):
            match = re.search(r'"Quolture"\s+(\d+)', data['lines'][0])
            if match:
                return (puzzle_name, match.group(1))
        return (puzzle_name, hash(data.get('raw_text', '')))

    # Fallback for unknown puzzle types
    return (puzzle_name, hash(data.get('raw_text', '')))


def deduplicate_puzzles(puzzles: List[Dict]) -> List[Dict]:
    """
    Remove duplicate puzzles, keeping only the first occurrence.

    Uses _get_puzzle_identity() to determine uniqueness.
    For Pips, same puzzle number but different difficulties are NOT duplicates.

    Args:
        puzzles: List of puzzle dictionaries

    Returns:
        List with duplicates removed
    """
    seen_identities = set()
    unique_puzzles = []

    for puzzle in puzzles:
        identity = _get_puzzle_identity(puzzle)
        if identity not in seen_identities:
            seen_identities.add(identity)
            unique_puzzles.append(puzzle)

    return unique_puzzles


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

    for puzzle in puzzles:
        # Check if puzzle is pre-formatted (e.g., combined Pips)
        if 'formatted' in puzzle:
            formatted = puzzle['formatted']
        else:
            formatter = puzzle['formatter']
            data = puzzle['data']
            # Format this puzzle
            formatted = formatter.format(data)

        # Determine if this is a multi-line puzzle (Wordle)
        is_multiline = '\n' in formatted

        # Add blank line before Wordle if there were previous puzzles
        if (is_multiline or puzzle['puzzle_name'] == 'pips') and formatted_parts:
            formatted_parts.append('')  # Blank line separator

        formatted_parts.append(formatted)

    return '\n'.join(formatted_parts)


def aggregate_pips_puzzles(puzzles: List[Dict]) -> List[Dict]:
    """
    Combine multiple Pips puzzles into single entry.

    Multiple Pips puzzles (Easy, Medium, Hard) should be formatted as a single line:
    "Pips #XXX Easy 🟢 1:25 | Medium 🟡 5:52 | Hard 🔴 35:28"

    Args:
        puzzles: List of puzzle dictionaries (already sorted)

    Returns:
        List with consecutive Pips entries combined into single entry
    """
    if not puzzles:
        return puzzles

    result = []
    pips_group = []

    for puzzle in puzzles:
        if puzzle['puzzle_name'] == 'pips':
            pips_group.append(puzzle)
        else:
            # Not a Pips puzzle - flush any accumulated Pips first
            if pips_group:
                result.append(_combine_pips_group(pips_group))
                pips_group = []
            result.append(puzzle)

    # Flush remaining Pips group
    if pips_group:
        result.append(_combine_pips_group(pips_group))

    return result


def _combine_pips_group(pips_puzzles: List[Dict]) -> Dict:
    """
    Combine multiple Pips puzzle entries into single entry.

    Puzzles are sorted by difficulty (Easy, Medium, Hard) before combining.

    Args:
        pips_puzzles: List of Pips puzzle dictionaries

    Returns:
        Single combined puzzle dictionary
    """
    # Sort by difficulty before combining
    sorted_pips = sorted(
        pips_puzzles,
        key=lambda p: PIPS_DIFFICULTY_ORDER.get(p['data']['difficulty'], 999)
    )

    # Format each individual Pips puzzle
    formatted_parts = []
    for puzzle in sorted_pips:
        formatter = puzzle['formatter']
        data = puzzle['data']
        formatted = formatter.format(data)

        # Remove "Pips #XXX " prefix from all but the first
        if formatted_parts:
            # Extract just "Difficulty Emoji Time" part
            # Format is: "Pips #XXX Difficulty Emoji Time"
            parts = formatted.split(' ', 2)  # Split into ["Pips", "#XXX", "Difficulty Emoji Time"]
            if len(parts) >= 3:
                formatted = parts[2]  # Just "Difficulty Emoji Time"

        formatted_parts.append(formatted)

    # Join with " | " separator
    combined_formatted = ' | '.join(formatted_parts)

    # Return combined entry (keep first puzzle's metadata after sorting)
    first_puzzle = sorted_pips[0]
    return {
        'puzzle_name': 'pips',
        'formatter': first_puzzle['formatter'],
        'data': first_puzzle['data'],
        'formatted': combined_formatted  # Pre-formatted combined output
    }


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

    # Remove duplicates (keeps first occurrence)
    deduplicated_puzzles = deduplicate_puzzles(sorted_puzzles)

    # Aggregate multiple Pips puzzles into single entry
    aggregated_puzzles = aggregate_pips_puzzles(deduplicated_puzzles)

    # Format into final output
    output = format_output(aggregated_puzzles)

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

    while True:  # Outer loop - runs until quit
        try:
            while True:  # Inner loop - captures puzzles until Ctrl+C
                # Wait for Enter keypress or quit command
                user_input = input("Press Enter to capture (or type 'quit' to exit): ").strip().lower()

                # Check for quit command
                if user_input == 'quit':
                    print("Exiting...")
                    return

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
                print("No puzzles captured yet.")
                print()
                continue  # Return to outer loop instead of exiting

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

            print("\nResults ready to paste! Continue adding puzzles or type 'quit' to exit.")
            print()
            # Continue to outer loop - don't exit!


def main():
    """
    Main entry point: Run interactive mode with auto-copy to clipboard.
    """
    interactive_mode()


if __name__ == '__main__':
    main()

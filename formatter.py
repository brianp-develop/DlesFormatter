#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from __future__ import print_function, unicode_literals, absolute_import, division

import io
import json
import os
import re
import sys

# Configure stdout for UTF-8 on Windows to handle emoji properly.
# The sentinel prevents double-wrapping when both formatter and tests apply the
# Py2 codecs writer; double-wrap would feed UTF-8 bytes into a second encoder
# and crash on the implicit ASCII decode.
if sys.platform == 'win32' and not getattr(sys, '_dlesformatter_utf8_wrapped', False):
    if sys.version_info[0] >= 3:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    else:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout, errors='replace')
    sys._dlesformatter_utf8_wrapped = True

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
# A "---" entry in config.json's puzzle_order inserts a blank line in the
# output before the next puzzle. Multiple consecutive markers collapse to one.
BLANK_LINE_MARKER = '---'


def _parse_puzzle_order(puzzle_order):
    """Split a config puzzle_order list into puzzle names and blank-before set.

    Returns:
        (clean_order, blank_before_set)
        - clean_order: list of puzzle_name strings, in config order, markers stripped
        - blank_before_set: set of puzzle_names that should be preceded by a blank line
    """
    clean_order = []
    blank_before = set()
    pending_blank = False
    for entry in puzzle_order:
        if entry == BLANK_LINE_MARKER:
            pending_blank = True
        else:
            clean_order.append(entry)
            if pending_blank:
                blank_before.add(entry)
                pending_blank = False
    return clean_order, blank_before


def load_config():
    """
    Load configuration from config.json, or return defaults if missing.

    config.json is gitignored — copy config.json.example to config.json to
    customize ordering and blank-line markers. Without it, puzzles emit in
    detection order with no blank lines between them.

    Returns:
        Dictionary containing puzzle_order list (possibly empty)

    Raises:
        SystemExit if config.json exists but contains invalid JSON
    """
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

    if not os.path.exists(config_path):
        return {"puzzle_order": []}

    try:
        with io.open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except ValueError as e:
        # json.JSONDecodeError on Py3 (subclass of ValueError); plain ValueError on Py2
        print("Error: Invalid JSON in config.json: {}".format(e))
        sys.exit(1)


def split_into_puzzle_blocks(text):
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
        r'(?=^#numble\d+)',
        r'(?=^Word Bunny\s)',
        r'(?=^Cine2Nerdle\s+#)',
    ]

    text_with_delimiters = text
    for pattern in puzzle_headers:
        text_with_delimiters = re.sub(pattern, PUZZLE_SEPARATOR, text_with_delimiters, flags=re.MULTILINE)

    # Also split by URLs (remove URLs and create breaks)
    url_pattern = r'https?://[^\s]+'
    text_with_delimiters = re.sub(url_pattern, '\n{}\n'.format(PUZZLE_SEPARATOR), text_with_delimiters)

    # Split by the delimiter
    blocks = text_with_delimiters.split(PUZZLE_SEPARATOR)

    # Clean up blocks: remove empty ones and strip whitespace
    blocks = [block.strip() for block in blocks if block.strip()]

    return blocks


def detect_and_parse_puzzles(text):
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


def sort_puzzles_by_config(puzzles, puzzle_order):
    """
    Sort detected puzzles according to the configured order.

    Puzzles not in the config are placed at the end in order of detection.
    Also annotates each puzzle with a 'blank_before' flag derived from
    BLANK_LINE_MARKER entries in puzzle_order, which format_output reads.

    Args:
        puzzles: List of detected puzzle dictionaries
        puzzle_order: Ordered list of puzzle_name identifiers from config,
                      optionally interleaved with BLANK_LINE_MARKER entries

    Returns:
        Sorted list of puzzle dictionaries
    """
    clean_order, blank_before = _parse_puzzle_order(puzzle_order)

    def get_sort_key(puzzle):
        puzzle_name = puzzle['puzzle_name']
        try:
            return clean_order.index(puzzle_name)
        except ValueError:
            return UNKNOWN_PUZZLE_PRIORITY

    sorted_puzzles = sorted(puzzles, key=get_sort_key)

    for puzzle in sorted_puzzles:
        puzzle['blank_before'] = puzzle['puzzle_name'] in blank_before

    return sorted_puzzles


def _get_puzzle_identity(puzzle):
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

    elif puzzle_name == 'framed_titleshot':
        # Direct access to puzzle_number
        return (puzzle_name, data.get('puzzle_number', ''))

    elif puzzle_name == 'connections':
        # Direct access to puzzle_number
        return (puzzle_name, data.get('puzzle_number', ''))

    elif puzzle_name == 'strands':
        # Direct access to puzzle_number
        return (puzzle_name, data.get('puzzle_number', ''))

    elif puzzle_name == 'waffle':
        # Direct access to puzzle_number
        return (puzzle_name, data.get('puzzle_number', ''))

    elif puzzle_name == 'numble':
        # Direct access to puzzle_number
        return (puzzle_name, data.get('puzzle_number', ''))

    elif puzzle_name == 'word_bunny':
        # Word Bunny has no puzzle number; use the date line as identity
        return (puzzle_name, data.get('date', ''))

    elif puzzle_name in ('cine2nerdle_regular', 'cine2nerdle_reversal'):
        # Direct access to puzzle_number ('1283' for regular, 'R1112' for reversal)
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


def deduplicate_puzzles(puzzles):
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


def format_output(puzzles):
    """
    Format all puzzles into final output string.

    Blank lines between puzzles are driven by the 'blank_before' flag
    that sort_puzzles_by_config attaches based on "---" markers in
    config.json. By default puzzles are emitted back-to-back with no
    separator; insert a marker in config.json to add blank lines.

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
            formatted = formatter.format(data)

        if puzzle.get('blank_before') and formatted_parts:
            formatted_parts.append('')

        formatted_parts.append(formatted)

    return '\n'.join(formatted_parts)


def aggregate_pips_puzzles(puzzles):
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


def _combine_pips_group(pips_puzzles):
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


def process_puzzle_results(input_text):
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


def _format_and_copy(all_puzzles_text):
    """Format accumulated puzzles, print results, copy to clipboard.

    Preserves all_puzzles_text so the user can keep adding puzzles after
    formatting (incremental day-long capture).
    """
    print("\n")

    if not all_puzzles_text:
        print("No puzzles captured yet.")
        print()
        return

    combined_input = '\n\n'.join(all_puzzles_text)
    output = process_puzzle_results(combined_input)

    print("=== Formatted Results ===")
    print(output)
    print()

    try:
        pyperclip.copy(output)
        print("✓ Results copied to clipboard!")
    except Exception as e:
        print("Note: Could not copy to clipboard: {}".format(e))

    print("\nResults ready to paste! Continue adding puzzles or type 'quit' to exit.")
    print()


def interactive_mode():
    """
    Interactive mode: Read puzzles from clipboard one at a time.

    User workflow:
    1. Complete a puzzle and copy the result (Ctrl+C)
    2. Press Enter in this terminal to capture it
    3. Repeat for more puzzles throughout the day
    4. Type 'done' to format and copy all captured puzzles
    5. Continue adding more puzzles or type 'quit' to exit

    Note: 'done' is the trigger on the Py2.7 branch; Ctrl+C is treated as
    a hard exit because Py2.7 + Windows can deliver a deferred SIGINT into
    the recovery print and crash. Master also accepts Ctrl+C.
    """
    print("=== Puzzle Results Formatter ===")
    print("1. Complete a puzzle and copy the result (Ctrl+C)")
    print("2. Press Enter here to capture it")
    print("3. Repeat for more puzzles")
    print("4. Type 'done' to format all puzzles and copy to clipboard")
    print("5. Continue adding puzzles or type 'quit' to exit")
    print()

    all_puzzles_text = []

    # input() vs raw_input() bridge for Py2 compatibility
    try:
        prompt_input = raw_input  # Py2
    except NameError:
        prompt_input = input  # Py3

    while True:  # Loop until 'quit' or hard interrupt
        try:
            user_input = prompt_input("Press Enter to capture (or 'done' / 'quit'): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            # On Py2.7 we don't try to recover from Ctrl+C — just exit.
            print("")
            return

        if user_input == 'quit':
            print("Exiting...")
            return

        if user_input == 'done':
            _format_and_copy(all_puzzles_text)
            continue  # keep accumulating

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
            print("  ✓ Captured {}".format(formatter.puzzle_name.replace('_', ' ').title()))
            all_puzzles_text.append(clipboard_content)
        else:
            print("  ⚠ Unrecognized puzzle format (will try to process anyway)")
            all_puzzles_text.append(clipboard_content)

        print()


def main():
    """
    Main entry point: Run interactive mode with auto-copy to clipboard.
    """
    interactive_mode()


if __name__ == '__main__':
    main()

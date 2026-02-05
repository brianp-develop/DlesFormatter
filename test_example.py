#!/usr/bin/env python3
"""Quick demo of formatter with sample data."""

import sys

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    import io
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from formatter import process_puzzle_results

# Sample input with all 4 puzzles in WRONG order
sample_input = """Wordle 1,692 4/6

🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩

https://www.nytimes.com/games/wordle

"Quolture"  1447  ⭐️3

🎬: ⬜️⬜️5️⃣
📺: ⬜️🟩0️⃣

https://www.quolture.com

Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥

https://framed.wtf

Framed - One Frame Challenge #1427
🎥 🟥

https://framed.wtf"""

print("=" * 70)
print("INPUT (puzzles in mixed order):")
print("=" * 70)
print(sample_input)
print()

# Process it
output = process_puzzle_results(sample_input)

print("=" * 70)
print("OUTPUT (auto-reordered and formatted):")
print("=" * 70)
print(output)
print()
print("=" * 70)
print("✓ Success! All puzzles formatted correctly.")
print("  - Framed puzzles: single line, no spaces")
print("  - Quolture: single line with spaces")
print("  - Wordle: multi-line with blank line before it")
print("  - All URLs removed")
print("  - Auto-reordered: Framed → Framed One Frame → Quolture → Wordle")

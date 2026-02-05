# Quick Reference Card

## Daily Usage

### Option 1: Interactive Mode (Default)
```bash
python formatter.py
```
- Paste puzzle results as you complete them
- Press Enter on empty input when done
- Results auto-copied to clipboard

### Option 2: Clipboard Mode
```bash
python formatter.py -c
```
- Copy all results first
- Run command
- Formatted results auto-copied back

## Supported Puzzles

- ✅ Framed
- ✅ Framed One Frame Challenge
- ✅ Quolture
- ✅ Wordle

## What Gets Formatted

### Input (any order, any combination)
```
Wordle 1,692 4/6
🟩⬛🟩⬛⬛
...

Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥
...
```

### Output (auto-reordered)
```
Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥

Wordle 1,692 4/6
🟩⬛🟩⬛⬛
...
```

## Common Commands

```bash
# Get help
python formatter.py --help

# Verify installation
python verify_structure.py

# Run tests
python tests/test_formatter.py

# Interactive mode
python formatter.py

# Clipboard mode
python formatter.py -c
```

## Troubleshooting Quick Fixes

### Python not found
```bash
# Try these alternatives:
python3 formatter.py
py formatter.py
```

### Missing pyperclip
```bash
pip install pyperclip
# or
python -m pip install pyperclip
```

### Clipboard not working (Linux)
```bash
sudo apt-get install xclip
```

### Emoji display issues
- Use Windows Terminal or PowerShell (not Command Prompt)
- Ensure UTF-8 encoding

## Files You Might Edit

### Add a new puzzle
1. Create `puzzle_formatters/newpuzzle.py`
2. Edit `puzzle_formatters/__init__.py` (import + register)
3. Edit `config.json` (add to puzzle_order)

### Change puzzle order
Edit `config.json`:
```json
{
  "puzzle_order": [
    "framed_regular",
    "wordle",
    "quolture"
  ]
}
```

## Getting More Help

- **Installation**: See [SETUP.md](SETUP.md)
- **Usage examples**: See [docs/EXAMPLES.md](docs/EXAMPLES.md)
- **Adding puzzles**: See [docs/ADDING_PUZZLES.md](docs/ADDING_PUZZLES.md)
- **How it works**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Overview**: See [README.md](README.md)

## Typical Workflow

```
Morning ────────────────────────────────────────────── Evening

  │                                                        │
  │  Complete     Complete      Complete     Complete     │
  │  Framed       Wordle        Quolture     One Frame    │
  │     │            │              │            │        │
  │     └────────────┴──────────────┴────────────┘        │
  │                       │                               │
  │                  Paste all into                       │
  │                   formatter.py                        │
  │                       │                               │
  │                Auto-reordered &                       │
  │                   formatted                           │
  │                       │                               │
  │                Paste into Teams!                      │
  │                                                        │
  └────────────────────────────────────────────────────────┘
```

## Pro Tips

1. **Keep it running**: Start `formatter.py` in morning, paste as you go
2. **Create alias**: `alias puzzles='python /path/to/formatter.py -c'`
3. **Missing puzzles OK**: Only format what you completed today
4. **Order doesn't matter**: Paste in any order, output always consistent
5. **Batch processing**: Copy all at end of day, use `-c` flag

---

**That's it! Simple, fast, effective.** 🎯

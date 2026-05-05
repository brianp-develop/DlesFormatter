# Quick Reference Card

## Daily Usage

### Interactive Mode
```bash
python formatter.py
```
- Copy puzzle result (Ctrl+C from puzzle site)
- Press Enter in formatter terminal to capture
- Repeat for each puzzle
- Press Ctrl+C when done
- Results automatically copied to clipboard - paste into Teams!

## Supported Puzzles

- ✅ Framed
- ✅ Framed One Frame Challenge
- ✅ Quolture
- ✅ Wordle
- ✅ Connections
- ✅ Strands
- ✅ Pips (Easy 🟢, Medium 🟡, Hard 🔴)

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
# Run formatter
python formatter.py

# Verify installation
python verify_structure.py

# Run tests
python tests/test_formatter.py
```

## Troubleshooting Quick Fixes

### Python not found
```bash
# Try these alternatives:
python3 formatter.py
py formatter.py
```

### Missing dependencies
```bash
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

### Emoji display issues
- Use Windows Terminal or PowerShell (not Command Prompt)
- Ensure UTF-8 encoding

## Files You Might Edit

### Add a new puzzle
1. Create `puzzle_formatters/newpuzzle.py`
2. Edit `puzzle_formatters/__init__.py` (import + register)
3. Edit `config.json.example` (add to puzzle_order — this is the committed layout)

### Change puzzle order
`config.json` is gitignored — copy the example first if you don't have one:
```bash
cp config.json.example config.json
```
Then edit `config.json`. `puzzle_order` is a list of identifiers; insert `"---"` to add a blank line before the next puzzle:
```json
{
  "puzzle_order": [
    "framed_regular",
    "---",
    "wordle",
    "quolture"
  ]
}
```
Without a `config.json`, puzzles appear in detection order with no blank lines.

## Getting More Help

- **Installation**: See [README.md](README.md#installation)
- **Windows setup**: See [WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md)
- **Usage examples**: See [docs/EXAMPLES.md](docs/EXAMPLES.md)
- **Adding puzzles**: See [docs/ADDING_PUZZLES.md](docs/ADDING_PUZZLES.md)
- **How it works**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Typical Workflow

```
Morning ────────────────────────────────────────────── Evening

  │                                                        │
  │  Complete     Complete      Complete     Complete     │
  │  Framed       Wordle        Quolture     One Frame    │
  │     │            │              │            │        │
  │  Copy+Enter  Copy+Enter    Copy+Enter   Copy+Enter    │
  │     │            │              │            │        │
  │     └────────────┴──────────────┴────────────┘        │
  │                  (formatter.py                        │
  │                 running all day)                      │
  │                       │                               │
  │                   Ctrl+C to finish                    │
  │                       │                               │
  │                Auto-reordered &                       │
  │                 copied to clipboard                   │
  │                       │                               │
  │                Paste into Teams!                      │
  │                                                        │
  └────────────────────────────────────────────────────────┘
```

## Pro Tips

1. **Keep it running**: Start `formatter.py` in morning, paste as you go
2. **Create alias**: `alias puzzles='python /path/to/formatter.py'`
3. **Missing puzzles OK**: Only format what you completed today
4. **Order doesn't matter**: Paste in any order, output always consistent

---

**That's it! Simple, fast, effective.** 🎯

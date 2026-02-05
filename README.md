# Puzzle Results Formatter

A Python tool that collates and formats daily puzzle results (Wordle, Framed, Quolture, etc.) into a standardized format for sharing in Teams chat.

## Features

- **Flexible Input**: Paste puzzle results in any order
- **Missing Puzzle Handling**: Works with any combination of supported puzzles
- **Auto-Reordering**: Outputs puzzles in preferred order regardless of input order
- **Auto-Copy to Clipboard**: Formatted results automatically copied for easy sharing
- **Interactive Workflow**: Paste puzzles as you complete them throughout the day
- **Extensible**: Easy to add new puzzle types (see [docs/ADDING_PUZZLES.md](docs/ADDING_PUZZLES.md))
- **Windows Compatible**: Fully tested and optimized for Windows (see [WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md))

## Supported Puzzles

- **Framed** - Movie frame guessing game
- **Framed One Frame Challenge** - Single frame variant
- **Quolture** - Movie/TV quote trivia
- **Wordle** - Daily word puzzle
- **Connections** - NYT word grouping puzzle

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ready to use!**
   ```bash
   python formatter.py
   ```

## Usage

### Interactive Mode

Perfect for pasting results throughout the day as you complete puzzles:

```bash
python formatter.py
```

1. Run the script
2. Paste puzzle results (one at a time or all together)
3. Script automatically detects when each puzzle is complete
4. Press Ctrl+C when all puzzles are entered
5. Formatted results are displayed and **automatically copied to clipboard**
6. Paste into Teams!

**Note:** The script detects puzzle completion automatically by recognizing end markers (URLs for most puzzles, all-green row or 6 attempts for Wordle). Blank lines within puzzles are preserved.

## Example

### Input (any order)
```
Wordle 1,692 4/6

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
```

### Output (auto-reordered)
```
Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥
"Quolture"  1447  ⭐️3 🎬: ⬜️⬜️5️⃣ 📺: ⬜️🟩0️⃣

Wordle 1,692 4/6
🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩
```

## Configuration

Edit `config.json` to customize puzzle ordering:

```json
{
  "puzzle_order": [
    "framed_regular",
    "framed_oneframe",
    "quolture",
    "wordle"
  ]
}
```

## Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design and how it works
- **[ADDING_PUZZLES.md](docs/ADDING_PUZZLES.md)** - Tutorial for adding new puzzle types
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Input/output examples for all puzzles

## Troubleshooting

### Windows Users
See **[WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md)** for complete Windows-specific troubleshooting, including:
- UTF-8/emoji display issues
- Python installation problems
- Terminal recommendations
- Batch file setup

### Clipboard not working
- **Windows**: Works out of the box with pyperclip (see [WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md) if issues)
- **Linux**: Install `xclip` or `xsel`: `sudo apt-get install xclip`
- **Mac**: Should work out of the box

### Unicode/emoji display issues
- **Windows**: Use Windows Terminal or PowerShell (not cmd.exe) - see [WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md)
- **Linux/Mac**: Ensure your terminal supports UTF-8
- All platforms: Use a font with emoji support (Cascadia Code, Consolas, etc.)

### "No recognized puzzles found"
- Check that puzzle format matches examples in [docs/EXAMPLES.md](docs/EXAMPLES.md)
- Ensure you're pasting the complete puzzle result (title + grid + URL)

## License

Free to use and modify for personal use.

## Contributing

Want to add support for a new puzzle? See [docs/ADDING_PUZZLES.md](docs/ADDING_PUZZLES.md) for a step-by-step guide!

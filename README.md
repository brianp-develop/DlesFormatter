# Puzzle Results Formatter

A Python tool that collates and formats daily puzzle results (Wordle, Framed, Quolture, etc.) into a standardized format for sharing in Teams chat.

## Features

- **Flexible Input**: Paste puzzle results in any order
- **Missing Puzzle Handling**: Works with any combination of supported puzzles
- **Auto-Reordering**: Outputs puzzles in preferred order regardless of input order
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

### Quick Setup

1. **Check Python installation**
   ```bash
   python --version
   # or try: python3 --version
   # or try: py --version
   ```
   Need to install Python? See [detailed setup instructions](#detailed-setup) below.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If `pip` doesn't work, try:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python formatter.py
   ```
   You should see the interactive mode prompt. Press Ctrl+C to exit.

### Detailed Setup

#### Installing Python

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- **Important:** Check "Add Python to PATH" during installation
- Restart your terminal after installation

**Mac:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

#### Creating Shortcuts

**Windows Terminal custom profile (Recommended):**

For the best experience on Windows, create a dedicated Windows Terminal profile:
1. Open Windows Terminal settings (Ctrl+,)
2. Click **"+ New profile"** button
3. Set command line to run `formatter.py` directly
4. **Important**: Turn OFF "Warn when pasting multiple lines" in Advanced settings

See [WINDOWS_COMPATIBILITY.md Method 4](WINDOWS_COMPATIBILITY.md#method-4-windows-terminal-custom-profile-recommended) for step-by-step instructions.

**Windows batch file:**
Create `puzzle_formatter.bat`:
```batch
@echo off
cd C:\path\to\DlesFormatter
python formatter.py
pause
```

**Mac/Linux alias:**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias puzzles='cd /path/to/DlesFormatter && python formatter.py'
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
5. Formatted results are displayed
6. Copy and paste into Teams!

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

Quick links to help you get started:

- **New to the project?** Start here with this README
- **Windows user?** See [WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md) for setup and troubleshooting
- **Need a quick reference?** Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for daily usage
- **Want to understand how it works?** Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Adding a new puzzle type?** Follow [docs/ADDING_PUZZLES.md](docs/ADDING_PUZZLES.md)
- **Need usage examples?** See [docs/EXAMPLES.md](docs/EXAMPLES.md)

## Troubleshooting

### Windows Users
See **[WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md)** for complete Windows-specific troubleshooting, including:
- UTF-8/emoji display issues
- Python installation problems
- Terminal recommendations
- Batch file setup

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

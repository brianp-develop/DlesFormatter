# Setup and Installation Guide

> **Windows Users:** This project is fully Windows-compatible! All scripts are configured for UTF-8/emoji support. For Windows-specific help, see [WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md).

## Prerequisites

### 1. Install Python

You need Python 3.7 or higher. Check if you have it:

```bash
python --version
# or
python3 --version
```

If Python is not installed:

#### Windows
- Download from [python.org](https://www.python.org/downloads/)
- During installation, **check "Add Python to PATH"**
- Restart your terminal after installation

#### Mac
```bash
brew install python3
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### 2. Install Dependencies

From the `DlesFormatter` directory:

```bash
pip install -r requirements.txt
```

Or if `pip` doesn't work:

```bash
python -m pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```

This installs `pyperclip` for clipboard functionality.

## Verify Installation

### Quick Test

Run the formatter with help flag:

```bash
python formatter.py --help
```

You should see usage information.

### Run Tests

```bash
python tests/test_formatter.py
```

You should see all tests passing.

### Test with Sample Data

1. Copy this sample puzzle result:
```
Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥

https://framed.wtf
```

2. Run the formatter in clipboard mode:
```bash
python formatter.py -c
```

3. Expected output:
```
Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥
```

## Troubleshooting

### "Python not found" error

**Windows:**
1. Reinstall Python from python.org
2. Check "Add Python to PATH" during installation
3. Restart terminal

**Alternative:** Use `py` command instead of `python`:
```bash
py formatter.py
```

### "No module named 'pyperclip'" error

Install the dependency:
```bash
pip install pyperclip
# or
python -m pip install pyperclip
```

### Clipboard not working

**Linux:**
Install clipboard utilities:
```bash
sudo apt-get install xclip
# or
sudo apt-get install xsel
```

**Mac/Windows:** Should work out of the box.

### Emoji display issues

**Windows:**
- Use **Windows Terminal** (recommended) or PowerShell
- Avoid Command Prompt (poor Unicode support)

**Terminal settings:**
- Ensure UTF-8 encoding is enabled
- Use a font that supports emoji (Consolas, Cascadia Code, etc.)

### "Permission denied" error

Make the script executable (Mac/Linux):
```bash
chmod +x formatter.py
```

## First Run

### Interactive Mode (Recommended)

```bash
python formatter.py
```

Follow the prompts:
1. Paste puzzle results
2. Press Enter on empty input when done
3. Formatted results displayed and copied to clipboard
4. Paste into Teams!

### Clipboard Mode

```bash
python formatter.py -c
```

1. Copy puzzle results first
2. Run the command
3. Formatted results auto-copied back
4. Paste into Teams!

## Daily Usage

### Option 1: Keep Script Running (Interactive)
```bash
# Morning: start the script
python formatter.py

# Throughout the day: paste results as you complete puzzles
# Press Enter on empty input when done
```

### Option 2: One-Shot Processing (Clipboard)
```bash
# Copy all puzzle results
# Run formatter
python formatter.py -c
# Paste into Teams
```

## Making it Even Easier

### Create an Alias (Mac/Linux)

Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias puzzles='cd /path/to/DlesFormatter && python formatter.py -c'
```

Then just run:
```bash
puzzles
```

### Create a Shortcut (Windows)

1. Create a `.bat` file:
```batch
@echo off
cd C:\Users\bcpierson\source\DlesFormatter
python formatter.py -c
pause
```

2. Save as `puzzle_formatter.bat`
3. Double-click to run!

### Add to PATH (Advanced)

Make the script available from anywhere:

1. Add shebang to `formatter.py` (already included):
```python
#!/usr/bin/env python3
```

2. Make executable (Mac/Linux):
```bash
chmod +x formatter.py
```

3. Add to PATH or create symlink:
```bash
sudo ln -s /path/to/DlesFormatter/formatter.py /usr/local/bin/puzzles
```

4. Run from anywhere:
```bash
puzzles -c
```

## Next Steps

1. ✅ Verify installation works
2. ✅ Test with sample data
3. ✅ Run full test suite
4. ✅ Try with your real puzzle results
5. 🎯 Add to your daily workflow!

See [README.md](README.md) for usage details and [docs/EXAMPLES.md](docs/EXAMPLES.md) for more examples.

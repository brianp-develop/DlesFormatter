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

Run the formatter:

```bash
python formatter.py
```

You should see the interactive mode prompt.

### Run Tests

```bash
python tests/test_formatter.py
```

You should see all tests passing.

### Test with Sample Data

1. Run the formatter:
```bash
python formatter.py
```

2. Paste this sample puzzle result:
```
Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥

https://framed.wtf
```

3. Press Ctrl+C to process

4. Expected output (auto-copied to clipboard):
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

### Interactive Mode

```bash
python formatter.py
```

Follow the prompts:
1. Paste puzzle results (one at a time or all together)
2. Press Ctrl+C when done
3. Formatted results displayed and auto-copied to clipboard
4. Paste into Teams!

## Daily Usage

```bash
# Start the script
python formatter.py

# Paste puzzle results as you complete them throughout the day
# Press Ctrl+C when done
# Results are automatically copied to clipboard
# Paste into Teams!
```

## Making it Even Easier

### Create an Alias (Mac/Linux)

Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias puzzles='cd /path/to/DlesFormatter && python formatter.py'
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
python formatter.py
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
puzzles
```

## Next Steps

1. ✅ Verify installation works
2. ✅ Test with sample data
3. ✅ Run full test suite
4. ✅ Try with your real puzzle results
5. 🎯 Add to your daily workflow!

See [README.md](README.md) for usage details and [docs/EXAMPLES.md](docs/EXAMPLES.md) for more examples.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python CLI tool that formats daily puzzle results (Wordle, Framed, Connections, etc.) for sharing in Teams chat. Built with a plugin-based architecture where each puzzle type is a self-contained formatter class.

## Essential Commands

### Development
```bash
# Run interactive mode (main workflow)
python formatter.py

# Install dependencies
pip install -r requirements.txt
# or: python -m pip install -r requirements.txt

# Run tests
python tests/test_formatter.py
# or: pytest tests/test_formatter.py
```

### Testing
- All 67 tests must pass before committing changes
- Test file: `tests/test_formatter.py`
- Tests organized by: unit tests per formatter, pipeline integration, edge cases, deduplication logic

## Core Architecture

### Plugin-Based Formatter System

**Registry pattern** (`puzzle_formatters/__init__.py`):
- `ALL_FORMATTERS` list contains all instantiated formatter objects
- `get_formatter_for_text(text)` iterates through formatters until match found
- Order in `ALL_FORMATTERS` matters for overlapping detection patterns

**Base class contract** (`puzzle_formatters/base.py`):
```python
class BasePuzzleFormatter(ABC):
    puzzle_name: str          # Unique identifier (e.g., "wordle")
    detection_pattern: str    # Regex for can_parse()

    @abstractmethod
    def can_parse(text: str) -> bool

    @abstractmethod
    def parse(text: str) -> Optional[dict]

    @abstractmethod
    def format(puzzle_data: dict) -> str
```

### Processing Pipeline

**Order matters** (`formatter.py` lines 392-424):
```
1. split_into_puzzle_blocks()    # Split by headers/URLs
2. detect_and_parse_puzzles()     # Map blocks to formatters
3. sort_puzzles_by_config()       # Order by config.json
4. deduplicate_puzzles()          # Remove duplicate captures
5. aggregate_pips_puzzles()       # Combine Pips difficulties
6. format_output()                # Final string assembly
```

**Key insight**: Configuration (`config.json`) drives output ordering, not code.

### Output Formatting Rules

**Blank line insertion** (`formatter.py` lines 267-305):
- Single-line puzzles (Framed, Quolture): No separators between them
- Multi-line puzzles (Wordle, Connections, Waffle, Strands): Blank line before each (if not first)
- Pips: Treated as multi-line for separator purposes
- Result: Compact single-line section at top, then blank line + multi-line section

### Deduplication Logic

**Identity extraction** (`formatter.py` lines 177-264):
- Most puzzles: `(puzzle_name, puzzle_number)`
- **Pips special case**: `(puzzle_name, puzzle_number, difficulty)` - different difficulties are different puzzles
- Keeps **first occurrence**, removes later duplicates
- Runs after sorting, before aggregation

### Pips Special Handling

**Two-stage processing**:
1. **Deduplication stage**: Each difficulty treated as separate puzzle
2. **Aggregation stage**: Consecutive Pips combined into single line with ` | ` separator

**Example**: `Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52 | Hard 🔴 35:28`

Combines in `aggregate_pips_puzzles()` (lines 308-389), sorted by difficulty (Easy → Medium → Hard).

## Adding New Puzzles

**Time required**: 5-15 minutes per puzzle

**Three required changes**:
1. Create formatter class in `puzzle_formatters/[puzzle_name].py`
   - Inherit from `BasePuzzleFormatter`
   - Implement `can_parse()`, `parse()`, `format()`
   - Set `puzzle_name` (must match config identifier)
   - Set `detection_pattern` (specific regex, avoid broad patterns)

2. Register in `puzzle_formatters/__init__.py`
   - Import the new formatter class
   - Add to `ALL_FORMATTERS` list (order matters!)
   - Add to `__all__` exports

3. Update `config.json`
   - Add puzzle identifier to `puzzle_order` array

**See**: `docs/ADDING_PUZZLES.md` for step-by-step guide with examples

## Important Patterns

### Detection Pattern Design
- Must be **specific** to avoid false matches
- Example good: `r"Connections\s*\nPuzzle #\d+"` (multiline)
- Example bad: `r"Puzzle #\d+"` (too broad, matches many puzzles)
- Order in `ALL_FORMATTERS` determines precedence for overlapping patterns

### Interactive Mode Completion
In interactive mode, puzzle input is read from the clipboard when you press Enter. The input continues to accumulate until you press Ctrl+C, which triggers processing and formatting. There is no automatic completion detection - you control when to process the accumulated puzzles.

### Multi-line vs Single-line Output
- **Single-line**: Join title + grid with spaces (Framed, Quolture)
- **Multi-line**: Preserve grid structure with newlines (Wordle, Connections, Waffle)
- **Collapsed multi-line**: Parse multi-line, output single-line (Strands collapses emoji grid)

### Interactive Mode Workflow

**Nested loop architecture** (`formatter.py` lines 427-507):
```
Outer loop (continues until 'quit')
  └─ Inner loop (captures puzzles until Ctrl+C)
      ├─ Read from clipboard on Enter
      ├─ Accumulate in all_puzzles_text[]
      └─ Ctrl+C → Process → Copy to clipboard → Return to outer loop
```

**State persistence**: `all_puzzles_text[]` accumulates across multiple Ctrl+C events, allowing incremental puzzle addition throughout the day.

## Windows Compatibility

**UTF-8 configuration** (`formatter.py` lines 26-28):
- `sys.stdout.reconfigure(encoding='utf-8')` for emoji display
- Tested on Windows Terminal, PowerShell
- See `WINDOWS_COMPATIBILITY.md` for detailed setup

## Configuration System

**`config.json`** defines puzzle ordering:
- `puzzle_order`: Array of puzzle identifiers
- Puzzles appear in config order (top to bottom)
- Unknown puzzles (not in config) append at end
- Users can customize without code changes

**Identifier matching**: `puzzle_name` in formatter class must match identifier in config.

## File Structure

```
puzzle_formatters/
├── __init__.py          # Registry (ALL_FORMATTERS, get_formatter_for_text)
├── base.py              # BasePuzzleFormatter abstract class
├── connections.py       # Multi-line with row analysis
├── framed.py            # Two variants: regular + One Frame
├── pips.py              # Individual parser (aggregation in pipeline)
├── quolture.py          # Single-line with space joining
├── strands.py           # Multi-line input, collapsed output
├── waffle.py            # 5x5 grid validation + streak
└── wordle.py            # Multi-line grid formatter

formatter.py             # Main CLI + processing pipeline
config.json              # Puzzle ordering configuration
tests/test_formatter.py  # 67 tests (unit + integration)
```

## Testing Requirements

**Before committing**:
- All 67 tests must pass
- Run: `python tests/test_formatter.py`

**When adding new puzzles**:
- Add unit tests for formatter (can_parse, parse, format)
- Add integration test with other puzzles
- Test edge cases (extra blanks, missing components, mixed order)

**Test organization**:
- Unit tests per formatter class
- `TestPipsAggregation` for special combining logic
- `TestDeduplication` for identity-based duplicate removal
- `TestFullPipeline` for multi-puzzle integration
- `TestFormatterRegistry` for detection accuracy

## Common Development Tasks

### Debugging Formatter Issues
1. Test detection pattern: Does `can_parse()` return True?
2. Inspect parsed dict: What's in `parse()` output?
3. Check formatted output: Does `format()` match expected?
4. Verify registration: Is formatter in `ALL_FORMATTERS`?
5. Check config: Is `puzzle_name` in `config.json` puzzle_order?

### Modifying Output Format
- Single-line puzzles: Edit `format()` in formatter class
- Multi-line puzzles: Edit `format()` + ensure `format_output()` preserves structure
- Blank line rules: Modify `format_output()` (lines 267-305)
- Puzzle ordering: Edit `config.json` puzzle_order

### Handling Special Cases
- **Aggregation needs**: Follow Pips pattern (individual formatter + pipeline aggregation)
- **Custom completion**: Add logic in formatter (like `_is_strands_complete()`)
- **Variant puzzles**: Create separate formatter classes (like Framed vs Framed One Frame)

## Critical Details

1. **Never break deduplication**: Changing identity extraction logic affects how duplicates are detected
2. **Pips difficulty order matters**: Easy (1) → Medium (2) → Hard (3) enforced in aggregation
3. **Detection order matters**: First match in `ALL_FORMATTERS` wins
4. **Config identifiers must match**: `puzzle_name` in class = identifier in `config.json`
5. **URL removal**: Always filter URLs in `parse()` methods

## Documentation Files

- `README.md` - User-facing usage guide
- `docs/ARCHITECTURE.md` - Deep dive on design decisions
- `docs/ADDING_PUZZLES.md` - Step-by-step guide for new puzzles
- `docs/EXAMPLES.md` - Input/output examples for each puzzle
- `WINDOWS_COMPATIBILITY.md` - Windows-specific setup/troubleshooting
- `QUICK_REFERENCE.md` - Daily usage cheatsheet

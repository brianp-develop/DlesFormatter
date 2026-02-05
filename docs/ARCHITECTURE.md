# Architecture Documentation

## Overview

The Puzzle Results Formatter uses a **plugin-based architecture** where each puzzle type is a self-contained formatter. This design makes adding new puzzles trivial and keeps the codebase maintainable.

## Design Principles

### 1. Extensibility First
The entire system is designed around the idea that adding new puzzle types should be **fast and simple**. No core logic changes required - just drop in a new formatter class.

### 2. Separation of Concerns
- **Formatters**: Know how to parse and format one specific puzzle type
- **Registry**: Discovers and manages formatters
- **Core Logic**: Orchestrates detection, sorting, and output assembly
- **CLI**: Handles user interaction and clipboard operations

### 3. Configuration Over Code
Puzzle ordering is defined in `config.json`, not hardcoded. Users can customize the output order without touching Python code.

## System Components

### Base Formatter Class (`puzzle_formatters/base.py`)

Abstract base class that defines the contract all formatters must follow:

```python
class BasePuzzleFormatter(ABC):
    puzzle_name: str          # Unique identifier
    detection_pattern: str    # Regex for identification

    @abstractmethod
    def can_parse(text: str) -> bool:
        """Returns True if this formatter handles this text"""

    @abstractmethod
    def parse(text: str) -> Optional[dict]:
        """Extracts puzzle data from text"""

    @abstractmethod
    def format(puzzle_data: dict) -> str:
        """Formats parsed data according to puzzle rules"""
```

**Why this design?**
- Clear interface makes implementing new formatters straightforward
- Each formatter is self-contained and testable in isolation
- Type hints and docstrings guide developers

### Concrete Formatters

Each puzzle type has its own formatter:

- `FramedFormatter` - Regular Framed puzzle
- `FramedOneFrameFormatter` - One Frame variant
- `QuoltureFormatter` - Quolture puzzle
- `WordleFormatter` - Wordle puzzle

**Key implementation details:**

1. **Detection**: Each formatter has a unique regex pattern
   - Avoids conflicts (e.g., Framed vs Framed One Frame)
   - Handles variations in puzzle titles

2. **Parsing**: Extracts relevant lines from input
   - Filters out URLs automatically
   - Strips whitespace and blank lines
   - Returns structured data (dict)

3. **Formatting**: Applies puzzle-specific rules
   - Single-line puzzles: Concatenate title + grid
   - Multi-line puzzles: Preserve grid structure
   - No URLs in output

### Formatter Registry (`puzzle_formatters/__init__.py`)

Auto-discovery system for formatters:

```python
ALL_FORMATTERS = [
    FramedFormatter(),
    FramedOneFrameFormatter(),
    QuoltureFormatter(),
    WordleFormatter(),
]

def get_formatter_for_text(text: str):
    """Try each formatter until one matches"""
    for formatter in ALL_FORMATTERS:
        if formatter.can_parse(text):
            return formatter
    return None
```

**Why this design?**
- New formatters automatically available when imported
- No manual registration needed
- Easy to debug (all formatters in one list)

### Core Processing Pipeline (`formatter.py`)

The main script orchestrates the entire process:

#### 1. Input Splitting
```python
split_into_puzzle_blocks(text) -> List[str]
```
- Splits input by URLs (each puzzle ends with a URL)
- Returns individual text blocks for parsing

#### 2. Puzzle Detection
```python
detect_and_parse_puzzles(text) -> List[Dict]
```
- For each block, finds matching formatter
- Parses puzzle data
- Returns list of detected puzzles with metadata

#### 3. Sorting
```python
sort_puzzles_by_config(puzzles, puzzle_order) -> List[Dict]
```
- Reorders puzzles according to `config.json`
- Puzzles not in config appear at end (in detection order)
- Ensures consistent output regardless of input order

#### 4. Output Assembly
```python
format_output(puzzles) -> str
```
- Formats each puzzle using its formatter
- Adds blank line before Wordle (multi-line puzzle)
- No blank lines between single-line puzzles

## Data Flow

```
User Input
    ↓
[Split into blocks]
    ↓
[Detect puzzles] → Registry → Formatters
    ↓
[Parse each puzzle]
    ↓
[Sort by config]
    ↓
[Format output]
    ↓
Formatted Result → Clipboard
```

## Configuration System

`config.json` defines puzzle ordering:

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

**Benefits:**
- Users can customize order without code changes
- Easy to add new puzzles to ordering
- Clear separation of preferences vs logic

## CLI Design

### Interactive Mode
- Stays running, accepts multiple pastes
- User pastes as they complete puzzles throughout the day
- Accumulates all input, processes on exit
- Displays formatted results for copying
- Good for incremental puzzle completion

**Implementation:**
- Runs directly when script is executed (`python formatter.py`)
- Uses the core processing pipeline
- Results displayed for manual copying

## Error Handling

### Graceful Degradation
- **Missing puzzles**: Only formats puzzles that are present
- **Unknown formats**: Silently ignored (no crashes)
- **Empty input**: Clear error message

### User Feedback
- Shows number of lines captured in interactive mode
- Displays formatted output before copying to clipboard
- Clear error messages with actionable guidance

## Why This Architecture?

### Strengths
1. **Easy to extend**: Add new puzzle = one new file
2. **Testable**: Each formatter is independent
3. **Maintainable**: Clear responsibilities per module
4. **Flexible input**: Handles missing puzzles, any order
5. **User-friendly**: Interactive workflow for daily use

### Trade-offs
1. **More files**: Each puzzle needs its own file (worth it for maintainability)
2. **Some duplication**: Each formatter has similar structure (but customizable)

## Future Extensibility

The architecture supports future enhancements:

- **Custom formatting rules**: Add `format_template` to config
- **Puzzle variants**: Easy to handle multiple versions of same puzzle
- **Output formats**: Could support Slack, Discord, etc. with different formatters
- **Validation**: Could add puzzle result validation (score ranges, grid patterns)
- **History tracking**: Could save results to file with dates

**Want to add a new puzzle?** See [ADDING_PUZZLES.md](ADDING_PUZZLES.md) for a step-by-step guide.

## Testing Strategy

The architecture enables comprehensive testing:

1. **Unit tests**: Test each formatter independently
   - `can_parse()` with valid/invalid inputs
   - `parse()` with various formats
   - `format()` with edge cases

2. **Integration tests**: Test full pipeline
   - Mixed puzzle inputs
   - Different orderings
   - Missing puzzles

3. **Regression tests**: Real-world examples
   - Saved in `docs/EXAMPLES.md`
   - Ensure consistent behavior

## Code Style

All code follows these principles:

- **Type hints**: Function signatures have types
- **Docstrings**: All classes and methods documented
- **Comments**: Explain "why", not "what"
- **Naming**: Clear, descriptive variable/function names
- **DRY**: Shared logic in base class

## Performance Considerations

Current design is optimized for **correctness and maintainability** over raw performance, because:

1. **Small input size**: Processing a few KB of text
2. **Interactive use**: Human-in-the-loop, speed not critical
3. **Readability matters**: Code will be modified (adding puzzles)

If processing 1000s of puzzles, consider:
- Caching compiled regex patterns
- Parallel parsing of blocks
- Lazy evaluation

But for current use case (1-4 puzzles daily), simplicity wins.

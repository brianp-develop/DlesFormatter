# Adding New Puzzles - Step-by-Step Guide

This guide walks you through adding support for a new puzzle type. The process takes about 5-15 minutes per puzzle.

**Background reading:** For context on the system design, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Prerequisites

- Basic Python knowledge
- Understanding of regex (for puzzle detection)
- Sample puzzle result to work from

## Step 1: Analyze the Puzzle Format

Before writing code, understand the puzzle's structure:

### Questions to Answer
1. **What's the title format?** (e.g., "Connections Puzzle #123")
2. **How many lines?** (single-line result vs multi-line grid)
3. **Are there URLs?** (most puzzles include a link)
4. **What should be kept?** (title, score, emoji grid?)
5. **What should be removed?** (URLs, blank lines?)
6. **Single-line or multi-line output?**

### Example Analysis: "Connections"

```
Input:
Connections
Puzzle #245
🟪🟪🟪🟪
🟦🟦🟦🟦
🟩🟩🟩🟩
🟨🟨🟨🟨

https://www.nytimes.com/games/connections

Desired Output:
Connections Puzzle #245 🟪🟪🟪🟪 🟦🟦🟦🟦 🟩🟩🟩🟩 🟨🟨🟨🟨
```

**Analysis:**
- Title: "Connections" on line 1, "Puzzle #245" on line 2
- Grid: 4 lines of emoji squares
- URL: Standard NYT Games URL
- Output: Single line (title + grid collapsed)

## Step 2: Create the Formatter Class

Create a new file in `puzzle_formatters/` directory.

**File naming convention:** `puzzle_name.py` (lowercase, underscores for spaces)

### Template

```python
"""
Formatter for [Puzzle Name] puzzle.

Brief description of what this puzzle is.
Describe the formatting rules applied.
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class [PuzzleName]Formatter(BasePuzzleFormatter):
    """
    Formatter for [Puzzle Name] puzzle.

    Input format:
        [Paste example input here]

    Output format:
        [Show expected output here]
    """

    # Unique identifier (lowercase, underscores)
    puzzle_name = "puzzle_identifier"

    # Regex pattern to detect this puzzle
    detection_pattern = r"Pattern to match puzzle title"

    # Regex pattern indicating puzzle completion (for interactive mode)
    end_marker_pattern = r"Pattern to match completion indicator"

    def can_parse(self, text: str) -> bool:
        """Check if text contains [Puzzle Name] puzzle."""
        return bool(re.search(self.detection_pattern, text))

    def parse(self, text: str) -> Optional[dict]:
        """
        Extract [Puzzle Name] puzzle data.

        Returns:
            dict with relevant keys, or None if parsing fails
        """
        # Split text into lines and clean up
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

        # Filter out URL lines
        lines = [line for line in lines if not line.startswith('http')]

        # Validate minimum content
        if len(lines) < MINIMUM_EXPECTED_LINES:
            return None

        # Extract components
        # ... your parsing logic here ...

        return {
            'component1': value1,
            'component2': value2,
            'raw_text': text
        }

    def format(self, puzzle_data: dict) -> str:
        """
        Format as [single-line / multi-line] output.

        Example: [Show example output]
        """
        # Apply formatting rules
        # ... your formatting logic here ...

        return formatted_string
```

## Step 3: Define Class Attributes

### 3.1 Puzzle Name

Unique identifier (lowercase, underscores):
```python
puzzle_name = "connections"
```

This must match the identifier used in `config.json`.

### 3.2 Detection Pattern

Create a regex that uniquely identifies your puzzle:

```python
# Good patterns (specific)
detection_pattern = r"Connections\s+Puzzle #\d+"
detection_pattern = r"Semantle #\d+"
detection_pattern = r"Tradle #\d+ \d+/\d+"

# Avoid vague patterns (too generic)
detection_pattern = r"Puzzle \d+"  # Matches too many things!
detection_pattern = r"#\d+"         # Way too broad
```

**Testing tip:** Use [regex101.com](https://regex101.com) to test your pattern against sample inputs.

### 3.3 End Marker Pattern (Optional but Recommended)

Pattern that indicates the puzzle input is complete. Used in interactive mode to automatically detect when a puzzle has been fully pasted.

```python
# Most puzzles: URL pattern
end_marker_pattern = r"https://www\.example\.com"

# Wordle: All-green row (successful solve)
end_marker_pattern = r"🟩🟩🟩🟩🟩"

# Puzzle without URL: Final line pattern
end_marker_pattern = r"Score: \d+/\d+"
```

**Common end markers:**
- **URL-based** (most puzzles): Match the puzzle's URL
- **Content-based** (Wordle): Match final grid row or success indicator
- **Score-based**: Match final score line if puzzle has no URL

**Why this matters:** Without an end marker, interactive mode can't detect when the puzzle is complete, requiring the user to manually signal completion. With an end marker, the paste automatically completes when detected.

**Special handling:** Wordle has special logic that also completes after 6 emoji rows (failed solve), so you don't need to add that to the pattern.

### 3.4 Parse Method

Extract the components you need:

```python
def parse(self, text: str) -> Optional[dict]:
    """Extract puzzle components."""

    # 1. Split into lines and clean
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

    # 2. Remove URLs
    lines = [line for line in lines if not line.startswith('http')]

    # 3. Validate structure
    if len(lines) < 2:  # Minimum expected lines
        return None

    # 4. Extract components
    title = lines[0]          # Usually first line
    grid = lines[1:]          # Remaining lines
    # ... more extraction as needed ...

    # 5. Return structured data
    return {
        'title': title,
        'grid': grid,
        'raw_text': text
    }
```

**Common patterns:**
- Title is usually first non-empty line
- Grids are multiple lines of emojis
- Scores/stats are usually on title line or separate line

### 3.5 Format Method

Apply the formatting rules:

```python
def format(self, puzzle_data: dict) -> str:
    """Format according to puzzle rules."""

    # Single-line output
    if SINGLE_LINE_OUTPUT:
        parts = [puzzle_data['title']]
        parts.extend(puzzle_data['grid'])
        return ' '.join(parts)

    # Multi-line output
    if MULTI_LINE_OUTPUT:
        result = [puzzle_data['title']]
        result.extend(puzzle_data['grid'])
        return '\n'.join(result)
```

**Formatting guidelines:**
- Single-line: Join with spaces
- Multi-line: Join with newlines
- No URLs in output
- No unnecessary blank lines

## Step 4: Register the Formatter

Edit `puzzle_formatters/__init__.py`:

```python
# 1. Import your new formatter
from .connections import ConnectionsFormatter  # Add this line

# 2. Add to ALL_FORMATTERS list
ALL_FORMATTERS = [
    FramedFormatter(),
    FramedOneFrameFormatter(),
    QuoltureFormatter(),
    WordleFormatter(),
    ConnectionsFormatter(),  # Add this line
]

# 3. Add to __all__ list
__all__ = [
    'BasePuzzleFormatter',
    'FramedFormatter',
    'FramedOneFrameFormatter',
    'QuoltureFormatter',
    'WordleFormatter',
    'ConnectionsFormatter',  # Add this line
    'ALL_FORMATTERS',
    'get_formatter_for_text',
    'get_formatter_by_name',
]
```

## Step 5: Update Configuration

Edit `config.json` to add your puzzle to the ordering:

```json
{
  "puzzle_order": [
    "framed_regular",
    "framed_oneframe",
    "quolture",
    "connections",
    "wordle"
  ]
}
```

**Note:** The identifier here must match the `puzzle_name` in your formatter class.

## Step 6: Test Your Formatter

### Manual Testing

```bash
# Test with sample input
python formatter.py
# Paste your puzzle result
# Verify output looks correct
```

### Test Checklist
- [ ] Puzzle is detected correctly
- [ ] Title is extracted properly
- [ ] Grid/scores are formatted correctly
- [ ] URLs are removed
- [ ] Output matches expected format
- [ ] Works with other puzzles (mixed input)
- [ ] Handles missing optional components gracefully

### Edge Cases to Test
- Puzzle with unusual spacing
- Puzzle with extra blank lines
- Mixed with other puzzles in random order
- Only this puzzle (no others)

## Step 7: Document Your Addition

### Update README.md

Add your puzzle to the supported list:

```markdown
## Supported Puzzles

- **Framed** - Movie frame guessing game
- **Framed One Frame Challenge** - Single frame variant
- **Quolture** - Movie/TV quote trivia
- **Wordle** - Daily word puzzle
- **Connections** - Word grouping puzzle  <!-- Add this -->
```

### Update EXAMPLES.md

Add a complete input/output example (see Step 8).

## Step 8: Add Example to Documentation

Edit `docs/EXAMPLES.md`:

```markdown
## Connections

### Input
\```
Connections
Puzzle #245
🟪🟪🟪🟪
🟦🟦🟦🟦
🟩🟩🟩🟩
🟨🟨🟨🟨

https://www.nytimes.com/games/connections
\```

### Output
\```
Connections Puzzle #245 🟪🟪🟪🟪 🟦🟦🟦🟦 🟩🟩🟩🟩 🟨🟨🟨🟨
\```

### Formatting Rules
- Collapse title (two lines) into single "Connections Puzzle #N"
- Join all grid lines with spaces
- Remove URL
- Single-line output
```

## Complete Example: Adding "Connections"

### File: `puzzle_formatters/connections.py`

```python
"""
Formatter for Connections puzzle.

Connections is a word grouping puzzle from NYT Games.
Results are condensed to a single line.
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class ConnectionsFormatter(BasePuzzleFormatter):
    """
    Formatter for Connections puzzle.

    Input format:
        Connections
        Puzzle #245
        🟪🟪🟪🟪
        🟦🟦🟦🟦
        🟩🟩🟩🟩
        🟨🟨🟨🟨

        https://www.nytimes.com/games/connections

    Output format:
        Connections Puzzle #245 🟪🟪🟪🟪 🟦🟦🟦🟦 🟩🟩🟩🟩 🟨🟨🟨🟨
    """

    puzzle_name = "connections"
    detection_pattern = r"Connections\s+Puzzle #\d+"
    end_marker_pattern = r"https://www\.nytimes\.com/games/connections"

    def can_parse(self, text: str) -> bool:
        """Check if text contains Connections puzzle."""
        return bool(re.search(self.detection_pattern, text))

    def parse(self, text: str) -> Optional[dict]:
        """
        Extract Connections puzzle data.

        Returns:
            dict with 'title_lines' and 'grid_lines', or None if parsing fails
        """
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

        # Filter out URLs
        lines = [line for line in lines if not line.startswith('http')]

        if len(lines) < 2:
            return None

        # First two lines form the title
        title_line1 = lines[0]  # "Connections"
        title_line2 = lines[1]  # "Puzzle #245"

        # Remaining lines are the grid
        grid_lines = lines[2:]

        return {
            'title_line1': title_line1,
            'title_line2': title_line2,
            'grid_lines': grid_lines,
            'raw_text': text
        }

    def format(self, puzzle_data: dict) -> str:
        """
        Format as single line: "Connections Puzzle #N" + grid.

        Example: Connections Puzzle #245 🟪🟪🟪🟪 🟦🟦🟦🟦 🟩🟩🟩🟩 🟨🟨🟨🟨
        """
        # Combine title lines
        title = f"{puzzle_data['title_line1']} {puzzle_data['title_line2']}"

        # Join all parts with spaces
        parts = [title] + puzzle_data['grid_lines']
        return ' '.join(parts)
```

## Common Pitfalls

### 1. Detection Pattern Too Broad
**Bad:** `r"Puzzle #\d+"` (matches many puzzles)
**Good:** `r"Connections\s+Puzzle #\d+"` (specific to Connections)

### 2. Not Handling Variations
Some puzzles have multiple formats (like Framed vs Framed One Frame). Make sure your `can_parse()` distinguishes them.

### 3. Forgetting URLs
Always filter out URL lines in `parse()`:
```python
lines = [line for line in lines if not line.startswith('http')]
```

### 4. Not Validating Input
Always check minimum expected lines:
```python
if len(lines) < MINIMUM_LINES:
    return None
```

### 5. Puzzle Name Mismatch
The `puzzle_name` in your class MUST match the identifier in `config.json`.

## Debugging Tips

### Print Intermediate Results
```python
def parse(self, text: str) -> Optional[dict]:
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    print(f"DEBUG: Found {len(lines)} lines")  # Temporary debug
    print(f"DEBUG: Lines = {lines}")             # Temporary debug
    # ... rest of method
```

### Test Detection Pattern Separately
```python
import re
text = "Your sample puzzle text here"
pattern = r"Your pattern here"
print(bool(re.search(pattern, text)))  # Should print True
```

### Use Interactive Python
```python
python -i formatter.py
>>> from puzzle_formatters.connections import ConnectionsFormatter
>>> cf = ConnectionsFormatter()
>>> text = """paste your sample here"""
>>> cf.can_parse(text)
>>> cf.parse(text)
>>> cf.format(cf.parse(text))
```

## Summary

To add a new puzzle:

1. ✅ Analyze puzzle format
2. ✅ Create formatter class in `puzzle_formatters/`
3. ✅ Implement `can_parse()`, `parse()`, `format()`
4. ✅ Register in `__init__.py`
5. ✅ Add to `config.json`
6. ✅ Test with sample inputs
7. ✅ Update documentation

**Estimated time:** 5-15 minutes per puzzle

The plugin architecture makes this process straightforward and repeatable!

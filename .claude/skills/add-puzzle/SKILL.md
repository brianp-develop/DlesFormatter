---
name: add-puzzle
description: Add a new puzzle formatter to the DlesFormatter project. Use when the user wants to add support for a new puzzle type.
argument-hint: [paste raw puzzle example text, desired output format, and any special notes]
disable-model-invocation: true
---

# Add New Puzzle Formatter

You are adding a new puzzle type to the DlesFormatter project.

## Gathering Inputs

Before any implementation, you need to collect the required information from the user. If `$ARGUMENTS` already contains all the needed info (raw example, desired output, and notes), skip ahead to Step 1. Otherwise, conduct an **interview** — ask for ONE piece of information at a time using the AskUserQuestion tool, wait for the answer, then ask the next question. Do NOT ask multiple questions at once.

**Interview sequence:**

1. **Raw puzzle example**: "Please paste a raw example of the puzzle results, exactly as copied from the puzzle website/app."
2. **Desired output format**: "Now paste or describe what the formatted output should look like for that example."
3. **Output position**: "Where should this puzzle appear in the output order? The current order is: `[list current puzzle_order from config.json]`. Should it go before or after a specific puzzle?"
4. **Output type**: "Is the output single-line (compact, like Framed/Quolture) or multi-line (preserves grid structure, like Wordle/Connections/Waffle)?"
5. **Special handling**: "Any special handling needed? For example: multiple variants (like Framed vs One Frame), aggregation across difficulties (like Pips Easy/Medium/Hard), or anything else unusual? If none, just say 'no'."

After collecting all answers, summarize what you gathered and confirm with the user before proceeding to Step 1.

## Implementation Steps

Follow these steps IN ORDER. Do not skip any step.

### Step 1: Analyze the Puzzle

From the user's example, determine:
- **Puzzle name** (lowercase, underscores for spaces) - confirm with user
- **Class name** (PascalCase + "Formatter")
- **Detection pattern** - a specific regex that uniquely identifies this puzzle. Must NOT be too broad.
- **Title format** - what the header/title line looks like
- **Grid/content format** - emoji grid, scores, times, etc.
- **URLs to strip** - any URLs that appear in the raw input
- **Output type** - single-line (like Framed/Quolture) or multi-line (like Wordle/Connections/Waffle)
- **Identity fields** - what makes this puzzle unique for deduplication (usually puzzle_name + puzzle_number)

Present your analysis to the user and get confirmation before proceeding.

### Step 2: Create the Formatter Class

Create `puzzle_formatters/<puzzle_name>.py` following this pattern:

```python
"""
Formatter for <Puzzle Name> puzzle.

<Brief description of the puzzle.>
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class <ClassName>Formatter(BasePuzzleFormatter):
    """
    Formatter for <Puzzle Name> puzzle.

    Input format:
        <paste the raw example>

    Output format:
        <paste the desired output>
    """

    puzzle_name = "<puzzle_identifier>"
    detection_pattern = r"<specific regex>"

    def can_parse(self, text: str) -> bool:
        """Check if text contains <Puzzle Name> puzzle."""
        return re.search(self.detection_pattern, text) is not None

    def parse(self, text: str) -> Optional[dict]:
        """
        Extract <Puzzle Name> puzzle data.

        Returns:
            dict with relevant keys, or None if parsing fails
        """
        lines = self._parse_lines(text)

        # Filter out URL lines
        lines = [line for line in lines if not line.startswith('http')]

        # ... extraction logic ...

        return {
            # Include 'puzzle_number' if the puzzle has one (needed for deduplication)
            'raw_text': text
        }

    def format(self, puzzle_data: dict) -> str:
        """Format as <single-line / multi-line> output."""
        # ... formatting logic ...
```

Key rules:
- Always filter URLs in `parse()`
- Always include `raw_text` in the returned dict
- Include `puzzle_number` in the dict if the puzzle has a number (needed for deduplication)
- Use `self._parse_lines(text)` for standard line splitting
- Return `None` from `parse()` if minimum structure validation fails

### Step 3: Register the Formatter

Edit `puzzle_formatters/__init__.py`:
1. Add import at the top with the other imports
2. Add instance to `ALL_FORMATTERS` list (order matters - more specific patterns before broad ones)
3. Add to `__all__` list

### Step 4: Update config.json

Add the puzzle identifier to `puzzle_order` array at the position the user specified. The identifier MUST match the `puzzle_name` attribute in the formatter class.

### Step 5: Update formatter.py

Two updates needed:

**5a. Add puzzle header pattern** to `split_into_puzzle_blocks()` (around line 83-91):
Add a regex pattern to the `puzzle_headers` list that matches the start of this puzzle's results. This allows the splitter to separate this puzzle from adjacent puzzles in pasted text.

**5b. Add identity extraction** to `_get_puzzle_identity()` (around line 177-239):
Add an `elif` case for this puzzle's `puzzle_name`. Extract the puzzle number (or other unique identifier) from the parsed data. Pattern:
```python
elif puzzle_name == '<identifier>':
    return (puzzle_name, data.get('puzzle_number', ''))
```

### Step 6: Write Tests

Add tests to `tests/test_formatter.py`:

1. **Add sample input constant(s)** at the top of the file with the other constants (FRAMED_INPUT, WORDLE_INPUT, etc.). Include the raw puzzle text. If there are variants or edge cases, add separate constants for each.

2. **Add test class** following the naming pattern `Test<ClassName>Formatter`:

Required tests (minimum):
- `test_can_parse_valid_input` - detection works
- `test_parse_extracts_components` - all fields extracted correctly
- `test_format_output` - formatted output matches expected
- `test_format_removes_urls` - URLs are stripped
- `test_formatter_registry` - registered and detectable via `get_formatter_for_text()`

Recommended additional tests:
- `test_can_parse_with_extra_blanks` - handles messy whitespace
- `test_parse_rejects_invalid` - returns None for bad input
- Edge case tests for any variants or special handling

3. **Add integration test** to `TestFullPipeline` class that tests this puzzle mixed with other puzzles.

4. **Add the test class** to the `test_classes` list in the `if __name__ == '__main__'` block at the bottom.

5. **Add the import** to the imports section at the top of the test file.

### Step 7: Run Tests

Run `python tests/test_formatter.py` and verify ALL tests pass (existing + new). Fix any failures before proceeding.

### Step 8: Stage Files

Stage all modified and new files with `git add`:
- `puzzle_formatters/<puzzle_name>.py` (new)
- `puzzle_formatters/__init__.py` (modified)
- `config.json` (modified)
- `formatter.py` (modified)
- `tests/test_formatter.py` (modified)

Do NOT commit - the user wants to test manually first.

### Step 9: Summary

Report:
- New formatter class and file path
- Detection pattern used
- Puzzle identifier and config position
- Number of new tests added
- Total test count (should be previous total + new tests)
- All tests passing confirmation
- Files staged (remind user to test and commit when ready)

## Important Rules

- Follow existing code style exactly (docstrings, spacing, naming)
- Detection patterns must be SPECIFIC - avoid broad patterns that could match other puzzles
- Always test that existing tests still pass after changes
- The `puzzle_name` in the class MUST match the identifier in `config.json`
- Do NOT update documentation files (README, EXAMPLES, ADDING_PUZZLES) unless the user asks

$ARGUMENTS

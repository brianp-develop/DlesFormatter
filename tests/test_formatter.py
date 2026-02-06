"""
Unit tests for puzzle formatters.

Tests individual formatters and the full processing pipeline.
Run with: python -m pytest tests/test_formatter.py
"""

import sys
from pathlib import Path

# Configure stdout for UTF-8 on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add parent directory to path to import puzzle_formatters
sys.path.insert(0, str(Path(__file__).parent.parent))

from puzzle_formatters import (
    ConnectionsFormatter,
    FramedFormatter,
    FramedOneFrameFormatter,
    PipsFormatter,
    QuoltureFormatter,
    StrandsFormatter,
    WaffleFormatter,
    WordleFormatter,
    get_formatter_for_text
)


# Sample puzzle inputs
FRAMED_INPUT = """Framed #1427
🎥 🟥 🟥 🟥 🟥 🟥 🟥

https://framed.wtf"""

FRAMED_ONEFRAME_INPUT = """Framed - One Frame Challenge #1427
🎥 🟥

https://framed.wtf"""

QUOLTURE_INPUT = """"Quolture"  1447  ⭐️3

🎬: ⬜️⬜️5️⃣
📺: ⬜️🟩0️⃣

https://www.quolture.com"""

WORDLE_INPUT = """Wordle 1,692 4/6

🟩⬛🟩⬛⬛
⬛⬛⬛⬛⬛
🟩🟨🟩⬛⬛
🟩🟩🟩🟩🟩"""

CONNECTIONS_INPUT = """Connections
Puzzle #970
🟦🟦🟦🟦
🟪🟪🟪🟪
🟩🟩🟩🟩
🟨🟨🟨🟨"""

CONNECTIONS_WITH_MIXED = """Connections
Puzzle #971
🟦🟪🟩🟨
🟦🟪🟨🟩
🟦🟦🟦🟦
🟪🟪🟪🟪
🟩🟩🟩🟩
🟨🟨🟨🟨"""

STRANDS_INPUT = """Strands #705
"Let's face it"
🟡🔵🔵🔵
🔵🔵🔵🔵"""

STRANDS_WITH_HINTS_INPUT = """Strands #706
"Game on"
💡🟡🔵🔵
🔵🔵💡🔵
🔵🔵"""

PIPS_EASY_INPUT = """Pips #173 Easy 🟢
1:25"""

PIPS_MEDIUM_INPUT = """Pips #171 Medium 🟡
5:52"""

PIPS_HARD_INPUT = """Pips #171 Hard 🔴
35:28"""

WAFFLE_INPUT = """#waffle1477 1/5



🟩🟩🟩🟩🟩
🟩⬜🟩⬜🟩
🟩🟩⭐🟩🟩
🟩⬜🟩⬜🟩
🟩🟩🟩🟩🟩



🔥 streak: 2

wafflegame.net"""

WAFFLE_NO_STREAK = """#waffle1478 3/5

🟩🟩🟩🟩🟩
🟩⬜🟩🟩🟩
🟩🟩⭐🟩🟩
🟩🟩🟩⬜🟩
🟩🟩🟩🟩🟩

wafflegame.net"""

WAFFLE_MANY_BLANKS = """#waffle1479 2/5




🟩🟩🟩🟩🟩
🟩⬜🟩⬜🟩


🟩🟩⭐🟩🟩


🟩⬜🟩⬜🟩
🟩🟩🟩🟩🟩




🔥 streak: 5



wafflegame.net"""


class TestFramedFormatter:
    """Tests for FramedFormatter."""

    def test_can_parse_valid_input(self):
        """Should detect valid Framed puzzle."""
        formatter = FramedFormatter()
        assert formatter.can_parse(FRAMED_INPUT) is True

    def test_can_parse_rejects_oneframe(self):
        """Should NOT detect Framed One Frame as regular Framed."""
        formatter = FramedFormatter()
        assert formatter.can_parse(FRAMED_ONEFRAME_INPUT) is False

    def test_parse_extracts_title_and_grid(self):
        """Should extract title and emoji grid."""
        formatter = FramedFormatter()
        result = formatter.parse(FRAMED_INPUT)

        assert result is not None
        assert result['title'] == 'Framed #1427'
        assert '🎥' in result['emoji_grid']
        assert '🟥' in result['emoji_grid']

    def test_format_creates_single_line(self):
        """Should format as single line: title + grid."""
        formatter = FramedFormatter()
        data = formatter.parse(FRAMED_INPUT)
        output = formatter.format(data)

        assert '\n' not in output  # Single line
        assert output.startswith('Framed #1427')
        assert '🎥' in output
        assert 'https' not in output  # URL removed


class TestFramedOneFrameFormatter:
    """Tests for FramedOneFrameFormatter."""

    def test_can_parse_valid_input(self):
        """Should detect valid One Frame puzzle."""
        formatter = FramedOneFrameFormatter()
        assert formatter.can_parse(FRAMED_ONEFRAME_INPUT) is True

    def test_can_parse_rejects_regular_framed(self):
        """Should NOT detect regular Framed as One Frame."""
        formatter = FramedOneFrameFormatter()
        assert formatter.can_parse(FRAMED_INPUT) is False

    def test_format_creates_single_line(self):
        """Should format as single line."""
        formatter = FramedOneFrameFormatter()
        data = formatter.parse(FRAMED_ONEFRAME_INPUT)
        output = formatter.format(data)

        assert '\n' not in output
        assert 'One Frame Challenge' in output
        assert 'https' not in output


class TestQuoltureFormatter:
    """Tests for QuoltureFormatter."""

    def test_can_parse_valid_input(self):
        """Should detect valid Quolture puzzle."""
        formatter = QuoltureFormatter()
        assert formatter.can_parse(QUOLTURE_INPUT) is True

    def test_parse_extracts_all_lines(self):
        """Should extract all non-URL lines."""
        formatter = QuoltureFormatter()
        result = formatter.parse(QUOLTURE_INPUT)

        assert result is not None
        assert len(result['lines']) >= 3  # Title + 2 grid lines minimum

    def test_format_creates_single_line(self):
        """Should format as single line with spaces."""
        formatter = QuoltureFormatter()
        data = formatter.parse(QUOLTURE_INPUT)
        output = formatter.format(data)

        assert '\n' not in output  # Single line
        assert '"Quolture"' in output
        assert '1447' in output
        assert '🎬:' in output
        assert '📺:' in output
        assert 'https' not in output


class TestWordleFormatter:
    """Tests for WordleFormatter."""

    def test_can_parse_valid_input(self):
        """Should detect valid Wordle puzzle."""
        formatter = WordleFormatter()
        assert formatter.can_parse(WORDLE_INPUT) is True

    def test_parse_extracts_title_and_grid(self):
        """Should extract title and grid lines."""
        formatter = WordleFormatter()
        result = formatter.parse(WORDLE_INPUT)

        assert result is not None
        assert 'Wordle' in result['title']
        assert '4/6' in result['title']
        assert len(result['grid_lines']) == 4  # 4 guesses

    def test_format_creates_multiline(self):
        """Should format as multi-line with title + grid."""
        formatter = WordleFormatter()
        data = formatter.parse(WORDLE_INPUT)
        output = formatter.format(data)

        lines = output.split('\n')
        assert len(lines) == 5  # Title + 4 grid lines
        assert 'Wordle' in lines[0]
        assert '🟩' in output
        assert 'https' not in output


class TestConnectionsFormatter:
    """Tests for ConnectionsFormatter."""

    def test_can_parse_valid_input(self):
        """Should detect valid Connections puzzle."""
        formatter = ConnectionsFormatter()
        assert formatter.can_parse(CONNECTIONS_INPUT) is True

    def test_parse_extracts_number_and_grid(self):
        """Should extract puzzle number and emoji grid."""
        formatter = ConnectionsFormatter()
        result = formatter.parse(CONNECTIONS_INPUT)

        assert result is not None
        assert result['puzzle_number'] == '970'
        assert len(result['grid_lines']) == 4  # 4 rows

    def test_format_creates_multiline(self):
        """Should format as multi-line with title + grid."""
        formatter = ConnectionsFormatter()
        data = formatter.parse(CONNECTIONS_INPUT)
        output = formatter.format(data)

        lines = output.split('\n')
        assert len(lines) == 5  # Title + 4 grid lines
        assert 'Connections #970' in lines[0]
        assert '🟦🟦🟦🟦' in output
        assert 'Puzzle' not in output  # "Puzzle #" removed in format

    def test_parse_handles_mixed_rows(self):
        """Should handle puzzles with mixed emoji rows."""
        formatter = ConnectionsFormatter()
        result = formatter.parse(CONNECTIONS_WITH_MIXED)

        assert result is not None
        assert result['puzzle_number'] == '971'
        assert len(result['grid_lines']) == 6  # 2 mixed + 4 solid rows

        # Check that mixed rows are included
        assert any('🟦🟪🟩🟨' in line for line in result['grid_lines'])

    def test_formatter_registry(self):
        """Should be registered and detectable by registry."""
        formatter = get_formatter_for_text(CONNECTIONS_INPUT)
        assert isinstance(formatter, ConnectionsFormatter)


class TestStrandsFormatter:
    """Tests for StrandsFormatter."""

    def test_can_parse_valid_input(self):
        """Should detect valid Strands puzzle."""
        formatter = StrandsFormatter()
        assert formatter.can_parse(STRANDS_INPUT) is True

    def test_parse_extracts_components(self):
        """Should extract puzzle number, theme, and emoji lines."""
        formatter = StrandsFormatter()
        result = formatter.parse(STRANDS_INPUT)

        assert result is not None
        assert result['puzzle_number'] == '705'
        assert result['theme'] == '"Let\'s face it"'
        assert len(result['emoji_lines']) == 2

    def test_format_collapses_emoji_grid(self):
        """Should collapse multi-line emoji grid to single line."""
        formatter = StrandsFormatter()
        data = formatter.parse(STRANDS_INPUT)
        output = formatter.format(data)

        lines = output.strip().split('\n')
        assert len(lines) == 3  # Title, theme, emoji line
        assert lines[0] == 'Strands #705'
        assert lines[1] == '"Let\'s face it"'
        assert lines[2] == '🟡🔵🔵🔵🔵🔵🔵🔵'
        assert '🟡' in lines[2]
        assert lines[2].count('🔵') == 7

    def test_handles_hints(self):
        """Should handle hint bulbs (💡) in emoji grid."""
        formatter = StrandsFormatter()
        result = formatter.parse(STRANDS_WITH_HINTS_INPUT)

        assert result is not None
        # Hints should be preserved in emoji lines
        all_emoji = ''.join(result['emoji_lines'])
        assert '💡' in all_emoji


class TestPipsFormatter:
    """Tests for PipsFormatter."""

    def test_can_parse_easy(self):
        """Should detect Pips Easy puzzle."""
        formatter = PipsFormatter()
        assert formatter.can_parse(PIPS_EASY_INPUT) is True

    def test_can_parse_medium(self):
        """Should detect Pips Medium puzzle."""
        formatter = PipsFormatter()
        assert formatter.can_parse(PIPS_MEDIUM_INPUT) is True

    def test_can_parse_hard(self):
        """Should detect Pips Hard puzzle."""
        formatter = PipsFormatter()
        assert formatter.can_parse(PIPS_HARD_INPUT) is True

    def test_parse_extracts_components_easy(self):
        """Should extract all components from Easy puzzle."""
        formatter = PipsFormatter()
        result = formatter.parse(PIPS_EASY_INPUT)

        assert result is not None
        assert result['puzzle_number'] == '173'
        assert result['difficulty'] == 'Easy'
        assert result['emoji'] == '🟢'
        assert result['time'] == '1:25'

    def test_parse_extracts_components_medium(self):
        """Should extract all components from Medium puzzle."""
        formatter = PipsFormatter()
        result = formatter.parse(PIPS_MEDIUM_INPUT)

        assert result is not None
        assert result['puzzle_number'] == '171'
        assert result['difficulty'] == 'Medium'
        assert result['emoji'] == '🟡'
        assert result['time'] == '5:52'

    def test_parse_extracts_components_hard(self):
        """Should extract all components from Hard puzzle."""
        formatter = PipsFormatter()
        result = formatter.parse(PIPS_HARD_INPUT)

        assert result is not None
        assert result['puzzle_number'] == '171'
        assert result['difficulty'] == 'Hard'
        assert result['emoji'] == '🔴'
        assert result['time'] == '35:28'

    def test_format_single_puzzle(self):
        """Should format single Pips puzzle as single line."""
        formatter = PipsFormatter()
        data = formatter.parse(PIPS_EASY_INPUT)
        output = formatter.format(data)

        assert output == 'Pips #173 Easy 🟢 1:25'
        assert '\n' not in output  # Single line

    def test_formatter_registry(self):
        """Should be registered and detectable by registry."""
        formatter = get_formatter_for_text(PIPS_EASY_INPUT)
        assert isinstance(formatter, PipsFormatter)


class TestPipsAggregation:
    """Tests for Pips puzzle aggregation logic."""

    def test_single_pips_puzzle(self):
        """Should handle single Pips puzzle (no aggregation needed)."""
        from formatter import process_puzzle_results

        output = process_puzzle_results(PIPS_EASY_INPUT)
        assert 'Pips #173 Easy 🟢 1:25' in output

    def test_two_pips_puzzles_combined(self):
        """Should combine two Pips puzzles into single line."""
        from formatter import process_puzzle_results

        mixed_input = f"""{PIPS_EASY_INPUT}

{PIPS_MEDIUM_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Should be combined into single line
        assert 'Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52' in output

        # Should only appear once (not twice)
        assert output.count('Pips') == 1

    def test_three_pips_puzzles_combined(self):
        """Should combine all three Pips puzzles into single line."""
        from formatter import process_puzzle_results

        mixed_input = f"""{PIPS_EASY_INPUT}

{PIPS_MEDIUM_INPUT}

{PIPS_HARD_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Should be combined into single line with all three
        assert 'Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52 | Hard 🔴 35:28' in output

        # Should only appear once
        assert output.count('Pips #') == 1

    def test_pips_with_other_puzzles(self):
        """Should handle Pips mixed with other puzzle types."""
        from formatter import process_puzzle_results

        mixed_input = f"""{WORDLE_INPUT}

{PIPS_EASY_INPUT}

{PIPS_MEDIUM_INPUT}

{STRANDS_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Should contain Wordle
        assert 'Wordle 1,692 4/6' in output

        # Should contain combined Pips
        assert 'Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52' in output

        # Should contain Strands
        assert 'Strands #705' in output

        # Pips should come after Strands (per config order)
        pips_idx = output.index('Pips')
        strands_idx = output.index('Strands')
        assert pips_idx > strands_idx

    def test_pips_out_of_order(self):
        """Should sort Pips by difficulty (Easy, Medium, Hard) regardless of input order."""
        from formatter import process_puzzle_results

        # Paste Medium before Easy (reversed order)
        # Note: Easy is #173, Medium is #171 (different puzzle numbers in test data)
        mixed_input = f"""{PIPS_MEDIUM_INPUT}

{PIPS_EASY_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Should be reordered: Easy first, then Medium
        # Uses puzzle number from first sorted entry (Easy #173)
        assert 'Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52' in output

    def test_pips_all_three_out_of_order(self):
        """Should sort all three Pips difficulties correctly."""
        from formatter import process_puzzle_results

        # Paste in random order: Hard, Easy, Medium
        # Note: Easy is #173, Medium/Hard are #171
        mixed_input = f"""{PIPS_HARD_INPUT}

{PIPS_EASY_INPUT}

{PIPS_MEDIUM_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Should be reordered: Easy, Medium, Hard
        # Uses puzzle number from first sorted entry (Easy #173)
        assert 'Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52 | Hard 🔴 35:28' in output


class TestWaffleFormatter:
    """Tests for WaffleFormatter."""

    def test_can_parse_valid_input(self):
        """Should detect valid Waffle puzzle."""
        formatter = WaffleFormatter()
        assert formatter.can_parse(WAFFLE_INPUT) is True

    def test_can_parse_no_streak(self):
        """Should detect Waffle without streak info."""
        formatter = WaffleFormatter()
        assert formatter.can_parse(WAFFLE_NO_STREAK) is True

    def test_can_parse_many_blanks(self):
        """Should detect Waffle with excessive blank lines."""
        formatter = WaffleFormatter()
        assert formatter.can_parse(WAFFLE_MANY_BLANKS) is True

    def test_parse_extracts_components(self):
        """Should extract title, puzzle number, grid, and streak."""
        formatter = WaffleFormatter()
        result = formatter.parse(WAFFLE_INPUT)

        assert result is not None
        assert result['title'] == '#waffle1477 1/5'
        assert result['puzzle_number'] == '1477'
        assert len(result['grid_lines']) == 5
        assert result['streak_info'] == '🔥 streak: 2'

    def test_parse_no_streak(self):
        """Should handle missing streak info gracefully."""
        formatter = WaffleFormatter()
        result = formatter.parse(WAFFLE_NO_STREAK)

        assert result is not None
        assert result['title'] == '#waffle1478 3/5'
        assert result['puzzle_number'] == '1478'
        assert len(result['grid_lines']) == 5
        assert result['streak_info'] is None

    def test_parse_validates_grid_size(self):
        """Should reject input without exactly 5 grid lines."""
        formatter = WaffleFormatter()

        invalid_input = """#waffle1477 1/5
🟩🟩🟩🟩🟩
🟩⬜🟩⬜🟩
🟩🟩⭐🟩🟩
wafflegame.net"""

        result = formatter.parse(invalid_input)
        assert result is None

    def test_format_with_streak(self):
        """Should format with streak info when present."""
        formatter = WaffleFormatter()
        data = formatter.parse(WAFFLE_INPUT)
        output = formatter.format(data)

        lines = output.strip().split('\n')
        assert len(lines) == 7  # Title + 5 grid + streak
        assert lines[0] == '#waffle1477 1/5'
        assert lines[1] == '🟩🟩🟩🟩🟩'
        assert lines[6] == '🔥 streak: 2'
        assert 'wafflegame.net' not in output

    def test_format_without_streak(self):
        """Should format without streak when absent."""
        formatter = WaffleFormatter()
        data = formatter.parse(WAFFLE_NO_STREAK)
        output = formatter.format(data)

        lines = output.strip().split('\n')
        assert len(lines) == 6  # Title + 5 grid (no streak)
        assert lines[0] == '#waffle1478 3/5'
        assert 'streak' not in output

    def test_format_removes_blank_lines(self):
        """Should remove all blank lines from output."""
        formatter = WaffleFormatter()
        data = formatter.parse(WAFFLE_MANY_BLANKS)
        output = formatter.format(data)

        assert '\n\n' not in output
        lines = output.strip().split('\n')
        assert all(line.strip() for line in lines)

    def test_formatter_registry(self):
        """Should be registered and detectable by registry."""
        formatter = get_formatter_for_text(WAFFLE_INPUT)
        assert isinstance(formatter, WaffleFormatter)

    def test_format_multiline_with_separator(self):
        """Should add blank line separator before Waffle in multi-puzzle output."""
        from formatter import process_puzzle_results

        mixed_input = f"""{FRAMED_INPUT}

{WAFFLE_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Should have blank line before Waffle (multi-line puzzle)
        assert '\n\n#waffle' in output


class TestFormatterRegistry:
    """Tests for formatter auto-detection."""

    def test_get_formatter_for_framed(self):
        """Should return FramedFormatter for Framed input."""
        formatter = get_formatter_for_text(FRAMED_INPUT)
        assert isinstance(formatter, FramedFormatter)

    def test_get_formatter_for_oneframe(self):
        """Should return FramedOneFrameFormatter for One Frame input."""
        formatter = get_formatter_for_text(FRAMED_ONEFRAME_INPUT)
        assert isinstance(formatter, FramedOneFrameFormatter)

    def test_get_formatter_for_quolture(self):
        """Should return QuoltureFormatter for Quolture input."""
        formatter = get_formatter_for_text(QUOLTURE_INPUT)
        assert isinstance(formatter, QuoltureFormatter)

    def test_get_formatter_for_wordle(self):
        """Should return WordleFormatter for Wordle input."""
        formatter = get_formatter_for_text(WORDLE_INPUT)
        assert isinstance(formatter, WordleFormatter)

    def test_get_formatter_returns_none_for_unknown(self):
        """Should return None for unrecognized input."""
        unknown_input = "This is not a valid puzzle result"
        formatter = get_formatter_for_text(unknown_input)
        assert formatter is None


class TestEdgeCases:
    """Tests for edge cases and unusual inputs."""

    def test_extra_blank_lines(self):
        """Should handle input with extra blank lines."""
        input_with_blanks = """Framed #1427


🎥 🟥 🟥 🟥 🟥 🟥 🟥


https://framed.wtf"""

        formatter = FramedFormatter()
        data = formatter.parse(input_with_blanks)
        output = formatter.format(data)

        assert output == 'Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥'

    def test_missing_blank_lines(self):
        """Should handle input with no blank lines."""
        input_no_blanks = """"Quolture"  1447  ⭐️3
🎬: ⬜️⬜️5️⃣
📺: ⬜️🟩0️⃣
https://www.quolture.com"""

        formatter = QuoltureFormatter()
        data = formatter.parse(input_no_blanks)
        output = formatter.format(data)

        assert '"Quolture"' in output
        assert '🎬:' in output
        assert '\n' not in output  # Single line

    def test_wordle_different_number_format(self):
        """Should handle Wordle with different number formats."""
        # Test with comma-separated number
        wordle_comma = "Wordle 1,692 4/6"
        formatter = WordleFormatter()
        assert formatter.can_parse(wordle_comma) is True

        # Test without comma
        wordle_no_comma = "Wordle 692 4/6"
        assert formatter.can_parse(wordle_no_comma) is True


# Integration test
class TestFullPipeline:
    """Tests for complete processing pipeline."""

    def test_all_puzzles_mixed_order(self):
        """Should correctly process all puzzles in mixed order."""
        # Import here to avoid circular dependency
        from formatter import process_puzzle_results

        mixed_input = f"""{WORDLE_INPUT}

{QUOLTURE_INPUT}

{FRAMED_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Should be reordered: Framed, Quolture, [blank], Wordle
        lines = output.split('\n')

        # First line should be Framed
        assert lines[0].startswith('Framed #1427')

        # Second line should be Quolture
        assert '"Quolture"' in lines[1]

        # Third line should be blank (before Wordle)
        assert lines[2] == ''

        # Fourth line should be Wordle title
        assert 'Wordle' in lines[3]

    def test_with_connections(self):
        """Should correctly process puzzles including Connections."""
        from formatter import process_puzzle_results

        mixed_input = f"""{WORDLE_INPUT}

{CONNECTIONS_INPUT}

{FRAMED_INPUT}"""

        output = process_puzzle_results(mixed_input)
        lines = output.split('\n')

        # Should be reordered: Framed, [blank], Wordle, [blank], Connections
        # First line should be Framed
        assert lines[0].startswith('Framed #1427')

        # Find Wordle and Connections in output
        output_text = '\n'.join(lines)
        assert 'Wordle 1,692 4/6' in output_text
        assert 'Connections #970' in output_text

        # Both Wordle and Connections should have blank lines before them
        assert '\n\nWordle' in output_text
        assert '\n\nConnections' in output_text

    def test_strands_in_mixed_input(self):
        """Should detect and format Strands among other puzzles."""
        from formatter import detect_and_parse_puzzles, sort_puzzles_by_config, format_output, load_config

        mixed_input = f"""{WORDLE_INPUT}

{CONNECTIONS_INPUT}

{STRANDS_INPUT}"""

        config = load_config()
        puzzles = detect_and_parse_puzzles(mixed_input)

        # Should find all 3 puzzles
        puzzle_names = [p['puzzle_name'] for p in puzzles]
        assert 'strands' in puzzle_names
        assert 'wordle' in puzzle_names
        assert 'connections' in puzzle_names

        # Strands should come after Connections in config order
        sorted_puzzles = sort_puzzles_by_config(puzzles, config['puzzle_order'])
        sorted_names = [p['puzzle_name'] for p in sorted_puzzles]
        strands_idx = sorted_names.index('strands')
        connections_idx = sorted_names.index('connections')
        assert strands_idx > connections_idx

        # Format output
        output = format_output(sorted_puzzles)

        # Strands should be multi-line with blank line separator before it
        assert 'Strands #705' in output
        assert '"Let\'s face it"' in output
        assert '\n\nStrands' in output  # Blank line before Strands

    def test_waffle_in_mixed_input(self):
        """Should detect and format Waffle among other puzzles."""
        from formatter import detect_and_parse_puzzles, sort_puzzles_by_config, format_output, load_config

        mixed_input = f"""{WORDLE_INPUT}

{CONNECTIONS_INPUT}

{WAFFLE_INPUT}"""

        config = load_config()
        puzzles = detect_and_parse_puzzles(mixed_input)

        # Should find all 3 puzzles
        puzzle_names = [p['puzzle_name'] for p in puzzles]
        assert 'waffle' in puzzle_names
        assert 'wordle' in puzzle_names
        assert 'connections' in puzzle_names

        # Waffle should come after Connections and Wordle
        sorted_puzzles = sort_puzzles_by_config(puzzles, config['puzzle_order'])
        sorted_names = [p['puzzle_name'] for p in sorted_puzzles]
        waffle_idx = sorted_names.index('waffle')
        connections_idx = sorted_names.index('connections')
        wordle_idx = sorted_names.index('wordle')
        assert waffle_idx > connections_idx
        assert waffle_idx > wordle_idx

        # Verify formatted output
        output = format_output(sorted_puzzles)
        assert '#waffle1477 1/5' in output
        assert '🔥 streak: 2' in output
        assert '\n\n#waffle' in output  # Blank line before Waffle


class TestDeduplication:
    """Tests for duplicate puzzle detection and removal."""

    def test_deduplicate_exact_wordle_duplicate(self):
        """Should remove exact Wordle duplicates, keeping only first occurrence."""
        from formatter import process_puzzle_results

        # Same Wordle pasted 3 times
        triple_input = f"""{WORDLE_INPUT}

{WORDLE_INPUT}

{WORDLE_INPUT}"""

        output = process_puzzle_results(triple_input)

        # Wordle should appear exactly once
        wordle_count = output.count('Wordle 1,692 4/6')
        assert wordle_count == 1, f"Expected Wordle to appear once, but appeared {wordle_count} times"

    def test_deduplicate_exact_framed_duplicate(self):
        """Should remove exact Framed duplicates."""
        from formatter import process_puzzle_results

        # Same Framed pasted 3 times
        triple_input = f"""{FRAMED_INPUT}

{FRAMED_INPUT}

{FRAMED_INPUT}"""

        output = process_puzzle_results(triple_input)

        # Framed should appear exactly once
        framed_count = output.count('Framed #1427')
        assert framed_count == 1, f"Expected Framed to appear once, but appeared {framed_count} times"

    def test_deduplicate_pips_same_difficulty(self):
        """Should remove duplicate Pips of same difficulty."""
        from formatter import process_puzzle_results

        # Pips Easy (x2) + Medium (x1)
        mixed_input = f"""{PIPS_EASY_INPUT}

{PIPS_EASY_INPUT}

{PIPS_MEDIUM_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Easy should appear once (not twice)
        # Output format: "Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52"
        assert 'Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52' in output
        # Verify Easy doesn't appear twice in the pipe-separated list
        assert output.count('Easy 🟢 1:25') == 1

    def test_no_deduplicate_pips_different_difficulty(self):
        """Should NOT deduplicate Pips with different difficulties - they're different puzzles."""
        from formatter import process_puzzle_results

        # Pips Easy + Medium (different difficulties, same or different puzzle numbers)
        combined_input = f"""{PIPS_EASY_INPUT}

{PIPS_MEDIUM_INPUT}"""

        output = process_puzzle_results(combined_input)

        # Both should be kept and combined
        assert 'Easy 🟢 1:25' in output
        assert 'Medium 🟡 5:52' in output
        # Should be on same line (pipe-separated)
        assert '|' in output

    def test_deduplicate_mixed_puzzles(self):
        """Should deduplicate mixed puzzle types correctly."""
        from formatter import process_puzzle_results

        # Multiple puzzle types with duplicates
        mixed_input = f"""{FRAMED_INPUT}

{WORDLE_INPUT}

{FRAMED_INPUT}

{CONNECTIONS_INPUT}

{CONNECTIONS_INPUT}

{WORDLE_INPUT}"""

        output = process_puzzle_results(mixed_input)

        # Each puzzle should appear exactly once
        assert output.count('Framed #1427') == 1
        assert output.count('Wordle 1,692 4/6') == 1
        assert output.count('Connections #970') == 1

    def test_deduplicate_keeps_first_occurrence(self):
        """Should keep first occurrence, not last."""
        from formatter import process_puzzle_results, detect_and_parse_puzzles, deduplicate_puzzles

        # Parse puzzles and check raw_text to verify first is kept
        triple_input = f"""{FRAMED_INPUT}

{FRAMED_INPUT}

{FRAMED_INPUT}"""

        puzzles = detect_and_parse_puzzles(triple_input)
        assert len(puzzles) == 3  # Three parsed

        deduplicated = deduplicate_puzzles(puzzles)
        assert len(deduplicated) == 1  # Only one kept

        # Verify it's the first one (all should be identical in this case, but order matters)
        assert deduplicated[0]['data']['raw_text'] == puzzles[0]['data']['raw_text']

    def test_no_deduplication_different_puzzle_numbers(self):
        """Should NOT deduplicate puzzles with different numbers (user catching up on old puzzles)."""
        from formatter import process_puzzle_results

        # Two different Wordle puzzles
        wordle_1692 = WORDLE_INPUT  # Wordle 1,692
        wordle_1693 = """Wordle 1,693 3/6

🟩⬛⬛⬛⬛
🟩🟩⬛⬛⬛
🟩🟩🟩🟩🟩"""

        combined_input = f"""{wordle_1692}

{wordle_1693}"""

        output = process_puzzle_results(combined_input)

        # Both should be kept (different puzzle numbers)
        assert 'Wordle 1,692' in output
        assert 'Wordle 1,693' in output

    def test_deduplicate_all_pips_difficulties_duplicated(self):
        """Should deduplicate when all three Pips difficulties are duplicated."""
        from formatter import process_puzzle_results

        # Easy (x2) + Medium (x2) + Hard (x2)
        # Note: Medium and Hard have same puzzle number (#171), Easy has #173
        all_duplicated = f"""{PIPS_EASY_INPUT}

{PIPS_EASY_INPUT}

{PIPS_MEDIUM_INPUT}

{PIPS_MEDIUM_INPUT}

{PIPS_HARD_INPUT}

{PIPS_HARD_INPUT}"""

        output = process_puzzle_results(all_duplicated)

        # Each difficulty should appear exactly once in the combined output
        # Format: "Pips #173 Easy 🟢 1:25 | Medium 🟡 5:52 | Hard 🔴 35:28"
        assert output.count('Easy 🟢 1:25') == 1
        assert output.count('Medium 🟡 5:52') == 1
        assert output.count('Hard 🔴 35:28') == 1
        # Should be combined with pipes
        assert 'Easy 🟢 1:25 | Medium 🟡 5:52 | Hard 🔴 35:28' in output


if __name__ == '__main__':
    print("Running tests manually (install pytest for better output)")
    print("=" * 60)

    # Run tests manually
    test_classes = [
        TestFramedFormatter,
        TestFramedOneFrameFormatter,
        TestQuoltureFormatter,
        TestWordleFormatter,
        TestConnectionsFormatter,
        TestStrandsFormatter,
        TestPipsFormatter,
        TestPipsAggregation,
        TestWaffleFormatter,
        TestDeduplication,
        TestFormatterRegistry,
        TestEdgeCases,
        TestFullPipeline,
    ]

    total_tests = 0
    passed_tests = 0

    for test_class in test_classes:
        print(f"\n{test_class.__name__}")
        print("-" * 60)

        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]

        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(instance, method_name)
                method()
                print(f"  ✓ {method_name}")
                passed_tests += 1
            except AssertionError as e:
                print(f"  ✗ {method_name}: {e}")
            except Exception as e:
                print(f"  ✗ {method_name}: Unexpected error: {e}")

    print("\n" + "=" * 60)
    print(f"Results: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"✗ {total_tests - passed_tests} tests failed")
        sys.exit(1)

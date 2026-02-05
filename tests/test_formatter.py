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
    FramedFormatter,
    FramedOneFrameFormatter,
    QuoltureFormatter,
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


if __name__ == '__main__':
    print("Running tests manually (install pytest for better output)")
    print("=" * 60)

    # Run tests manually
    test_classes = [
        TestFramedFormatter,
        TestFramedOneFrameFormatter,
        TestQuoltureFormatter,
        TestWordleFormatter,
        TestFormatterRegistry,
        TestEdgeCases,
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

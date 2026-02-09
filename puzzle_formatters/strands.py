"""
Formatter for NYT Strands puzzle results.

Strands is a word-finding game where players discover themed words.
Results show a multi-line emoji grid that gets collapsed to a single line.
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class StrandsFormatter(BasePuzzleFormatter):
    """
    Formatter for NYT Strands puzzle.

    Input format:
        Strands #705
        "Let's face it"
        🟡🔵🔵🔵
        🔵🔵🔵🔵

    Output format:
        Strands #705
        "Let's face it"
        🟡🔵🔵🔵🔵🔵🔵🔵

    Key characteristics:
    - Always has exactly 8 emoji: 7 blue (🔵) + 1 yellow (🟡)
    - May include hint bulbs (💡) that don't count toward completion
    - Multi-line grid collapses to single line
    - No URL for completion detection
    """

    puzzle_name = "strands"
    detection_pattern = r"Strands #\d+"

    def can_parse(self, text: str) -> bool:
        """
        Check if the text contains a Strands puzzle result.

        Args:
            text: The text to check

        Returns:
            True if text matches Strands format, False otherwise
        """
        return re.search(self.detection_pattern, text, re.MULTILINE) is not None

    def parse(self, text: str) -> Optional[dict]:
        """
        Parse Strands puzzle result from text.

        Expected format:
            Strands #705
            "Let's face it"
            🟡🔵🔵🔵
            🔵🔵🔵🔵

        Args:
            text: The text containing the puzzle result

        Returns:
            Dictionary with parsed data:
            - puzzle_number: The puzzle number
            - theme: The theme text (with quotes)
            - emoji_lines: List of emoji lines
            - raw_text: Original text for reference
        """
        lines = self._parse_lines(text)

        # Extract puzzle number from title
        puzzle_number = None
        title_line = None
        for line in lines:
            match = re.search(r'Strands #(\d+)', line)
            if match:
                puzzle_number = match.group(1)
                title_line = line
                break

        if not puzzle_number:
            return None

        # Extract theme line (starts with quote)
        theme = None
        for line in lines:
            if line.startswith('"') and line.endswith('"'):
                theme = line
                break

        # Extract emoji lines (contain Strands emoji: 🔵 🟡 💡)
        strands_emoji_pattern = r'^[🔵🟡💡]+$'
        emoji_lines = []
        for line in lines:
            if re.match(strands_emoji_pattern, line):
                emoji_lines.append(line)

        return {
            'puzzle_number': puzzle_number,
            'theme': theme,
            'emoji_lines': emoji_lines,
            'raw_text': text
        }

    def format(self, parsed_data: dict) -> str:
        """
        Format Strands puzzle result for output.

        Output format:
            Strands #705
            "Let's face it"
            🟡🔵🔵🔵🔵🔵🔵🔵

        Args:
            parsed_data: Dictionary from parse() method

        Returns:
            Formatted string (multi-line)
        """
        puzzle_number = parsed_data['puzzle_number']
        theme = parsed_data['theme']
        emoji_lines = parsed_data['emoji_lines']

        # Build output: title line, theme line, collapsed emoji grid
        output_lines = [f"Strands #{puzzle_number}"]

        if theme:
            output_lines.append(theme)

        # Collapse all emoji lines into single line
        if emoji_lines:
            collapsed_emoji = ''.join(emoji_lines)
            output_lines.append(collapsed_emoji)

        return '\n'.join(output_lines)

"""
Formatter for Quolture puzzle.

Quolture tests knowledge of movie and TV show quotes.
Results are condensed to a single line with all components separated by spaces.
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class QuoltureFormatter(BasePuzzleFormatter):
    """
    Formatter for Quolture puzzle.

    Input format:
        "Quolture"  1447  ⭐️3

        🎬: ⬜️⬜️5️⃣
        📺: ⬜️🟩0️⃣

        https://www.quolture.com

    Output format:
        "Quolture"  1447  ⭐️3 🎬: ⬜️⬜️5️⃣ 📺: ⬜️🟩0️⃣
    """

    puzzle_name = "quolture"
    detection_pattern = r'"Quolture"\s+\d+'
    end_marker_pattern = r"https://www\.quolture\.com"  # URL indicates puzzle completion

    def can_parse(self, text: str) -> bool:
        """Check if text contains Quolture puzzle."""
        return re.search(self.detection_pattern, text) is not None

    def parse(self, text: str) -> Optional[dict]:
        """
        Extract all Quolture puzzle components.

        Returns:
            dict with 'lines' key containing all non-URL lines, or None if parsing fails
        """
        lines = self._parse_lines(text)

        # Filter out URL lines
        lines = [line for line in lines if not line.startswith('http')]

        if len(lines) < 1:
            return None

        return {
            'lines': lines,
            'raw_text': text
        }

    def format(self, puzzle_data: dict) -> str:
        """
        Format as single line with all components joined by spaces.

        Example: "Quolture"  1447  ⭐️3 🎬: ⬜️⬜️5️⃣ 📺: ⬜️🟩0️⃣

        All lines are joined with single space separator.
        """
        return ' '.join(puzzle_data['lines'])

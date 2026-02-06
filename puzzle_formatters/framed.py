"""
Formatter for Framed and Framed One Frame puzzles.

Framed shows a movie through increasingly revealing frames.
Results are condensed to a single line: title + emoji grid.
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class FramedFormatter(BasePuzzleFormatter):
    """
    Formatter for regular Framed puzzle.

    Input format:
        Framed #1427
        🎥 🟥 🟥 🟥 🟥 🟥 🟥

        https://framed.wtf

    Output format:
        Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥
    """

    puzzle_name = "framed_regular"
    detection_pattern = r"Framed #\d+"
    end_marker_pattern = r"https://framed\.wtf"  # URL indicates puzzle completion

    def can_parse(self, text: str) -> bool:
        """Check if text contains regular Framed puzzle (not One Frame variant)."""
        # Must have "Framed #" but NOT "One Frame"
        has_framed = bool(re.search(self.detection_pattern, text))
        has_one_frame = "One Frame" in text
        return has_framed and not has_one_frame

    def parse(self, text: str) -> Optional[dict]:
        """
        Extract Framed puzzle title and emoji grid.

        Returns:
            dict with 'title' and 'emoji_grid' keys, or None if parsing fails
        """
        lines = self._parse_lines(text)

        # Filter out URL lines
        lines = [line for line in lines if not line.startswith('http')]

        if len(lines) < 2:
            return None

        # First line is title (e.g., "Framed #1427")
        title = lines[0]

        # Second line is emoji grid (e.g., "🎥 🟥 🟥 🟥 🟥 🟥 🟥")
        emoji_grid = lines[1]

        return {
            'title': title,
            'emoji_grid': emoji_grid,
            'raw_text': text
        }

    def format(self, puzzle_data: dict) -> str:
        """
        Format as single line: title immediately followed by emoji grid.

        Example: "Framed #1427🎥 🟥 🟥 🟥 🟥 🟥 🟥"
        """
        return f"{puzzle_data['title']}{puzzle_data['emoji_grid']}"


class FramedOneFrameFormatter(BasePuzzleFormatter):
    """
    Formatter for Framed - One Frame Challenge variant.

    Input format:
        Framed - One Frame Challenge #1427
        🎥 🟥

        https://framed.wtf

    Output format:
        Framed - One Frame Challenge #1427🎥 🟥
    """

    puzzle_name = "framed_oneframe"
    detection_pattern = r"Framed - One Frame Challenge #\d+"
    end_marker_pattern = r"https://framed\.wtf"  # URL indicates puzzle completion

    def can_parse(self, text: str) -> bool:
        """Check if text contains One Frame variant of Framed."""
        return re.search(self.detection_pattern, text) is not None

    def parse(self, text: str) -> Optional[dict]:
        """
        Extract One Frame puzzle title and emoji grid.

        Returns:
            dict with 'title' and 'emoji_grid' keys, or None if parsing fails
        """
        lines = self._parse_lines(text)

        # Filter out URL lines
        lines = [line for line in lines if not line.startswith('http')]

        if len(lines) < 2:
            return None

        # First line is title (e.g., "Framed - One Frame Challenge #1427")
        title = lines[0]

        # Second line is emoji grid (e.g., "🎥 🟥")
        emoji_grid = lines[1]

        return {
            'title': title,
            'emoji_grid': emoji_grid,
            'raw_text': text
        }

    def format(self, puzzle_data: dict) -> str:
        """
        Format as single line: title immediately followed by emoji grid.

        Example: "Framed - One Frame Challenge #1427🎥 🟥"
        """
        return f"{puzzle_data['title']}{puzzle_data['emoji_grid']}"

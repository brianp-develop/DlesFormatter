# -*- coding: utf-8 -*-
"""
Formatter for Framed - Title Shot Challenge puzzle.

Title Shot is a Framed variant where players guess the movie from a single
representative shot. Results are condensed to a single line: title + emoji grid.
"""

from __future__ import print_function, unicode_literals, absolute_import, division

import re
from .base import BasePuzzleFormatter


class FramedTitleShotFormatter(BasePuzzleFormatter):
    """
    Formatter for Framed - Title Shot Challenge variant.

    Input format:
        Framed - Title Shot Challenge #335
        🎥 🟥 🟥 🟩 ⬛ ⬛ ⬛

        https://framed.wtf/titleshot

    Output format:
        Framed - Title Shot Challenge #335🎥 🟥 🟥 🟩 ⬛ ⬛ ⬛
    """

    puzzle_name = "framed_titleshot"
    detection_pattern = r"Framed - Title Shot Challenge #\d+"

    def can_parse(self, text):
        """Check if text contains Title Shot variant of Framed."""
        return re.search(self.detection_pattern, text) is not None

    def parse(self, text):
        """
        Extract Title Shot puzzle title and emoji grid.

        Returns:
            dict with 'title', 'emoji_grid', and 'puzzle_number' keys, or None if parsing fails
        """
        lines = self._parse_lines(text)

        # Filter out URL lines
        lines = [line for line in lines if not line.startswith('http')]

        if len(lines) < 2:
            return None

        # First line is title (e.g., "Framed - Title Shot Challenge #335")
        title = lines[0]

        # Second line is emoji grid (e.g., "🎥 🟥 🟥 🟩 ⬛ ⬛ ⬛")
        emoji_grid = lines[1]

        # Extract puzzle number for deduplication
        match = re.search(r'#(\d+)', title)
        puzzle_number = match.group(1) if match else ''

        return {
            'title': title,
            'emoji_grid': emoji_grid,
            'puzzle_number': puzzle_number,
            'raw_text': text
        }

    def format(self, puzzle_data):
        """
        Format as single line: title immediately followed by emoji grid.

        Example: "Framed - Title Shot Challenge #335🎥 🟥 🟥 🟩 ⬛ ⬛ ⬛"
        """
        return "{}{}".format(puzzle_data['title'], puzzle_data['emoji_grid'])

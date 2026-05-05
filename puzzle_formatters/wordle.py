# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

"""
Formatter for Wordle puzzle.

Wordle is a word-guessing game with a 5-letter word.
Results keep the multi-line grid structure showing each guess.
"""

import re
from .base import BasePuzzleFormatter


class WordleFormatter(BasePuzzleFormatter):
    """
    Formatter for Wordle puzzle.

    Input format:
        Wordle 1,692 4/6

        🟩⬛🟩⬛⬛
        ⬛⬛⬛⬛⬛
        🟩🟨🟩⬛⬛
        🟩🟩🟩🟩🟩

    Output format:
        Wordle 1,692 4/6
        🟩⬛🟩⬛⬛
        ⬛⬛⬛⬛⬛
        🟩🟨🟩⬛⬛
        🟩🟩🟩🟩🟩

    Note: Keeps multi-line structure, removes blank line after title and URL.
    """

    puzzle_name = "wordle"
    detection_pattern = r"Wordle \d+[,\d]* \d+/\d+"

    def can_parse(self, text):
        """Check if text contains Wordle puzzle."""
        return re.search(self.detection_pattern, text) is not None

    def parse(self, text):
        """
        Extract Wordle title and emoji grid lines.

        Returns:
            dict with 'title' and 'grid_lines' keys, or None if parsing fails
        """
        lines = self._parse_lines(text)

        # Filter out URL lines
        lines = [line for line in lines if not line.startswith('http')]

        if len(lines) < 2:
            return None

        # First line is title (e.g., "Wordle 1,692 4/6")
        title = lines[0]

        # Remaining lines are the emoji grid (each guess)
        grid_lines = lines[1:]

        return {
            'title': title,
            'grid_lines': grid_lines,
            'raw_text': text
        }

    def format(self, puzzle_data):
        """
        Format as multi-line output: title on first line, then grid lines.

        Example:
            Wordle 1,692 4/6
            🟩⬛🟩⬛⬛
            ⬛⬛⬛⬛⬛
            🟩🟨🟩⬛⬛
            🟩🟩🟩🟩🟩
        """
        result = [puzzle_data['title']]
        result.extend(puzzle_data['grid_lines'])
        return '\n'.join(result)

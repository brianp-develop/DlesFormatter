# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

"""
Formatter for Pips puzzle.

Pips is a 3-part puzzle with Easy, Medium, and Hard difficulty levels.
Each difficulty generates its own result, but all captured Pips are combined
into a single output line.
"""

import re
from .base import BasePuzzleFormatter


class PipsFormatter(BasePuzzleFormatter):
    """
    Formatter for Pips puzzle (all difficulty levels).

    Input format (per difficulty):
        Pips #173 Easy 🟢
        1:25

    Output format (individual):
        Pips #173 Easy 🟢 1:25

    Note: Multiple Pips puzzles are aggregated into single line during
    final formatting (see process_puzzle_results).
    """

    puzzle_name = "pips"
    detection_pattern = r"Pips #\d+ (Easy|Medium|Hard)"

    def can_parse(self, text):
        """Check if text contains Pips puzzle (any difficulty)."""
        return re.search(self.detection_pattern, text) is not None

    def parse(self, text):
        """
        Extract Pips puzzle data.

        Returns:
            dict with 'puzzle_number', 'difficulty', 'emoji', 'time', or None
        """
        lines = self._parse_lines(text)

        if len(lines) < 2:
            return None

        # First line: "Pips #XXX [Difficulty] [Emoji]"
        title_line = lines[0]
        time_line = lines[1]

        # Extract puzzle number and difficulty
        match = re.search(r"Pips #(\d+) (Easy|Medium|Hard) (.)", title_line)
        if not match:
            return None

        puzzle_number = match.group(1)
        difficulty = match.group(2)
        emoji = match.group(3)

        return {
            'puzzle_number': puzzle_number,
            'difficulty': difficulty,
            'emoji': emoji,
            'time': time_line,
            'raw_text': text
        }

    def format(self, puzzle_data):
        """
        Format single Pips puzzle.

        Example: "Pips #173 Easy 🟢 1:25"

        Note: Multiple Pips puzzles are aggregated later in process_puzzle_results.
        """
        return "Pips #{} {} {} {}".format(
            puzzle_data['puzzle_number'],
            puzzle_data['difficulty'],
            puzzle_data['emoji'],
            puzzle_data['time'],
        )

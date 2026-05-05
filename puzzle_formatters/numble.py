# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

"""
Formatter for Numble puzzle results.

Numble is the number variant of Waffle from wafflegame.net, featuring a 7x7 grid.
Players rearrange numbers to form valid equations horizontally and vertically.
"""

import re
from .base import BasePuzzleFormatter


class NumbleFormatter(BasePuzzleFormatter):
    """
    Formatter for Numble puzzle.

    Input format:
        #numble9 0/5
        🟩🟩🟩🟩🟩🟩🟩
        🟩⬜🟩⬜🟩⬜🟩
        🟩🟩🟩🟩🟩🟩🟩
        🟩⬜🟩⬜🟩⬜🟩
        🟩🟩🟩🟩🟩🟩🟩
        🟩⬜🟩⬜🟩⬜🟩
        🟩🟩🟩🟩🟩🟩🟩
        wafflegame.net/numberwaffle

    Output format:
        #numble9 0/5
        🟩🟩🟩🟩🟩🟩🟩
        🟩⬜🟩⬜🟩⬜🟩
        🟩🟩🟩🟩🟩🟩🟩
        🟩⬜🟩⬜🟩⬜🟩
        🟩🟩🟩🟩🟩🟩🟩
        🟩⬜🟩⬜🟩⬜🟩
        🟩🟩🟩🟩🟩🟩🟩
        🔥 streak: 2
    """

    puzzle_name = "numble"
    detection_pattern = r"#numble\d+ \d+/5"

    def can_parse(self, text):
        """Check if text contains Numble puzzle."""
        return re.search(self.detection_pattern, text, re.MULTILINE) is not None

    def parse(self, text):
        """
        Extract Numble puzzle data.

        Returns dict with: title, puzzle_number, grid_lines (7 lines), streak_info (optional)
        """
        lines = self._parse_lines(text, filter_empty=False)

        # Extract title and puzzle number
        title = None
        puzzle_number = None
        for line in lines:
            match = re.search(r'(#numble(\d+) \d+/5)', line)
            if match:
                title = match.group(1)
                puzzle_number = match.group(2)
                break

        if not title:
            return None

        # Extract 7x7 emoji grid (exactly 7 lines)
        numble_emoji_pattern = r'^[🟩⬜⭐]{7}$'
        grid_lines = [line for line in lines if line and re.match(numble_emoji_pattern, line)]

        if len(grid_lines) != 7:
            return None

        # Extract optional streak info
        streak_info = None
        for line in lines:
            if line.startswith('🔥 streak:'):
                streak_info = line
                break

        return {
            'title': title,
            'puzzle_number': puzzle_number,
            'grid_lines': grid_lines,
            'streak_info': streak_info,
            'raw_text': text
        }

    def format(self, puzzle_data):
        """
        Format as multi-line: title + 7 grid lines + optional streak.

        Example output:
            #numble9 0/5
            🟩🟩🟩🟩🟩🟩🟩
            🟩⬜🟩⬜🟩⬜🟩
            🟩🟩🟩🟩🟩🟩🟩
            🟩⬜🟩⬜🟩⬜🟩
            🟩🟩🟩🟩🟩🟩🟩
            🟩⬜🟩⬜🟩⬜🟩
            🟩🟩🟩🟩🟩🟩🟩
            🔥 streak: 2
        """
        output_lines = [puzzle_data['title']]
        output_lines.extend(puzzle_data['grid_lines'])

        if puzzle_data['streak_info']:
            output_lines.append(puzzle_data['streak_info'])

        return '\n'.join(output_lines)

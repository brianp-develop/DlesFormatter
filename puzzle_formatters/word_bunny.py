# -*- coding: utf-8 -*-
"""
Formatter for Word Bunny puzzle results.

Word Bunny is a word ladder puzzle from wordbunny.app where players transform
one word into another through a chain of single-letter changes.
"""

from __future__ import print_function, unicode_literals, absolute_import, division

import re
from .base import BasePuzzleFormatter


class WordBunnyFormatter(BasePuzzleFormatter):
    """
    Formatter for Word Bunny puzzle.

    Input format:
        Word Bunny in 15 hops!
        5 MAY '26:
        WORST → BAD → GOOD → BEST
        🐰🐰🐰🐰🐰🐰|🐰🐰🐰|🐰🐰🐰🐰🐰🐰
        https://wordbunny.app/share

    Output format:
        Word Bunny in 15 hops!
        WORST → BAD → GOOD → BEST
        🐰🐰🐰🐰🐰🐰|🐰🐰🐰|🐰🐰🐰🐰🐰🐰
    """

    puzzle_name = "word_bunny"
    detection_pattern = r"Word Bunny in \d+ hops"

    def can_parse(self, text):
        """Check if text contains Word Bunny puzzle."""
        return re.search(self.detection_pattern, text) is not None

    def parse(self, text):
        """
        Extract Word Bunny puzzle data.

        Returns dict with: title, date, word_chain, bunny_grid

        Validation:
            - word_chain must contain exactly 3 arrows (→)
            - bunny_grid must contain exactly 2 pipe (|) characters
        """
        lines = self._parse_lines(text)

        # Filter out URL lines
        lines = [line for line in lines if not line.startswith('http')]

        # Extract title
        title = None
        title_pattern = r'Word Bunny in \d+ hops!?'
        for line in lines:
            match = re.match(title_pattern, line)
            if match:
                title = match.group(0)
                # Ensure trailing exclamation mark for consistent output
                if not title.endswith('!'):
                    title += '!'
                break

        if not title:
            return None

        # Extract date line (e.g., "5 MAY '26:")
        date = None
        date_pattern = r"^\d+\s+[A-Z]+\s+'\d+:?$"
        for line in lines:
            if re.match(date_pattern, line):
                date = line
                break

        # Extract word chain (line with exactly 3 arrows)
        word_chain = None
        for line in lines:
            if line.count('→') == 3:
                word_chain = line
                break

        if not word_chain:
            return None

        # Extract bunny grid (line with exactly 2 pipes and bunny emojis)
        bunny_grid = None
        for line in lines:
            if line.count('|') == 2 and '🐰' in line:
                bunny_grid = line
                break

        if not bunny_grid:
            return None

        return {
            'title': title,
            'date': date,
            'word_chain': word_chain,
            'bunny_grid': bunny_grid,
            'raw_text': text
        }

    def format(self, puzzle_data):
        """
        Format as multi-line: title + word chain + bunny grid.

        The date line is stripped from the output.

        Example output:
            Word Bunny in 15 hops!
            WORST → BAD → GOOD → BEST
            🐰🐰🐰🐰🐰🐰|🐰🐰🐰|🐰🐰🐰🐰🐰🐰
        """
        return '\n'.join([
            puzzle_data['title'],
            puzzle_data['word_chain'],
            puzzle_data['bunny_grid'],
        ])

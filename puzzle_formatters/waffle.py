"""
Formatter for Waffle puzzle results.

Waffle is a daily word puzzle game featuring a 5x5 grid of letters.
Players rearrange letters to form valid words horizontally and vertically.
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class WaffleFormatter(BasePuzzleFormatter):
    """Formatter for Waffle puzzle."""

    puzzle_name = "waffle"
    detection_pattern = r"#waffle\d+ \d+/5"
    end_marker_pattern = ""  # Uses content-based detection

    def can_parse(self, text: str) -> bool:
        """Check if text contains Waffle puzzle."""
        return re.search(self.detection_pattern, text, re.MULTILINE) is not None

    def parse(self, text: str) -> Optional[dict]:
        """
        Extract Waffle puzzle data.

        Returns dict with: title, puzzle_number, grid_lines (5 lines), streak_info (optional)
        """
        lines = self._parse_lines(text, filter_empty=False)

        # Extract title and puzzle number
        title = None
        puzzle_number = None
        for line in lines:
            match = re.search(r'(#waffle(\d+) \d+/5)', line)
            if match:
                title = match.group(1)
                puzzle_number = match.group(2)
                break

        if not title:
            return None

        # Extract 5x5 emoji grid (exactly 5 lines)
        waffle_emoji_pattern = r'^[🟩⬜⭐]{5}$'
        grid_lines = [line for line in lines if line and re.match(waffle_emoji_pattern, line)]

        if len(grid_lines) != 5:
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

    def format(self, puzzle_data: dict) -> str:
        """
        Format as multi-line: title + 5 grid lines + optional streak.

        Example output:
            #waffle1477 1/5
            🟩🟩🟩🟩🟩
            🟩⬜🟩⬜🟩
            🟩🟩⭐🟩🟩
            🟩⬜🟩⬜🟩
            🟩🟩🟩🟩🟩
            🔥 streak: 2
        """
        output_lines = [puzzle_data['title']]
        output_lines.extend(puzzle_data['grid_lines'])

        if puzzle_data['streak_info']:
            output_lines.append(puzzle_data['streak_info'])

        return '\n'.join(output_lines)

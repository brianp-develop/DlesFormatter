"""
Formatter for regular Cine2Nerdle puzzle results.

Cine2Nerdle is a daily film-trivia grid puzzle. Each guess fills a row with
colored cells indicating correctness. The Reversal variant uses an "R"
prefix on the puzzle number and is handled by a separate formatter.
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class Cine2NerdleRegularFormatter(BasePuzzleFormatter):
    """Formatter for regular Cine2Nerdle puzzle (numeric puzzle number)."""

    puzzle_name = "cine2nerdle_regular"
    detection_pattern = r"Cine2Nerdle\s+#\d+"

    GRID_LINE_PATTERN = r'^[⬜🟨🟥🟩⬛🟦🟧🟪]+$'

    def can_parse(self, text: str) -> bool:
        """Check if text contains regular Cine2Nerdle puzzle."""
        return re.search(self.detection_pattern, text) is not None

    def parse(self, text: str) -> Optional[dict]:
        """
        Extract Cine2Nerdle puzzle data.

        Returns dict with: title, puzzle_number, grid_lines, swaps_left
        """
        lines = self._parse_lines(text)
        lines = [line for line in lines if not line.startswith('http') and not line.startswith('www.')]

        title = None
        puzzle_number = None
        for line in lines:
            match = re.match(r'(Cine2Nerdle\s+#(\d+))', line)
            if match:
                title = match.group(1)
                puzzle_number = match.group(2)
                break

        if not title:
            return None

        grid_lines = [line for line in lines if re.match(self.GRID_LINE_PATTERN, line)]

        if not grid_lines:
            return None

        swaps_left = None
        for line in lines:
            if line.startswith('Swaps Left:'):
                swaps_left = line
                break

        return {
            'title': title,
            'puzzle_number': puzzle_number,
            'grid_lines': grid_lines,
            'swaps_left': swaps_left,
            'raw_text': text
        }

    def format(self, puzzle_data: dict) -> str:
        """
        Format as multi-line: title + grid lines + Swaps Left.

        Example output:
            Cine2Nerdle #1283
            ⬜🟨🟨🟨
            🟨🟨🟨⬜
            🟨🟨🟨⬜
            🟨🟨🟨⬜
            Swaps Left: 0
        """
        output_lines = [puzzle_data['title']]
        output_lines.extend(puzzle_data['grid_lines'])
        if puzzle_data['swaps_left']:
            output_lines.append(puzzle_data['swaps_left'])
        return '\n'.join(output_lines)

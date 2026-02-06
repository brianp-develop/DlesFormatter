"""
Formatter for NYT Connections puzzle results.

Connections is a word grouping game that displays results as colored emoji grids.
"""

import re
from typing import Optional
from .base import BasePuzzleFormatter


class ConnectionsFormatter(BasePuzzleFormatter):
    """Formatter for NYT Connections puzzle results."""

    puzzle_name = "connections"
    detection_pattern = r"Connections\s*\nPuzzle #\d+"
    end_marker_pattern = ""  # Uses content-based detection only

    def can_parse(self, text: str) -> bool:
        """
        Check if the text contains a Connections puzzle result.

        Args:
            text: The text to check

        Returns:
            True if text matches Connections format, False otherwise
        """
        return re.search(self.detection_pattern, text, re.MULTILINE) is not None

    def parse(self, text: str) -> Optional[dict]:
        """
        Parse Connections puzzle result from text.

        Expected format:
            Connections
            Puzzle #970
            🟦🟦🟦🟦
            🟪🟪🟪🟪
            🟩🟩🟩🟩
            🟨🟨🟨🟨

        Args:
            text: The text containing the puzzle result

        Returns:
            Dictionary with parsed data:
            - puzzle_number: The puzzle number
            - grid_lines: List of emoji grid lines
            - raw_text: Original text for reference
        """
        lines = self._parse_lines(text)

        # Extract puzzle number
        puzzle_number = None
        for line in lines:
            match = re.search(r'Puzzle #(\d+)', line)
            if match:
                puzzle_number = match.group(1)
                break

        # Extract grid lines (lines with Connections emojis)
        connections_emoji_pattern = r'^[🟦🟪🟩🟨]+$'
        grid_lines = []
        for line in lines:
            if re.match(connections_emoji_pattern, line):
                grid_lines.append(line)

        # Validate puzzle_number was found
        if not puzzle_number:
            return None

        return {
            'puzzle_number': puzzle_number,
            'grid_lines': grid_lines,
            'raw_text': text
        }

    def format(self, puzzle_data: dict) -> str:
        """
        Format Connections puzzle result for output.

        Output format:
            Connections #970
            🟦🟦🟦🟦
            🟪🟪🟪🟪
            🟩🟩🟩🟩
            🟨🟨🟨🟨

        Args:
            puzzle_data: Dictionary from parse() method

        Returns:
            Formatted string (multi-line)
        """
        puzzle_number = puzzle_data['puzzle_number']
        grid_lines = puzzle_data['grid_lines']

        # Build output: title line + grid rows
        output_lines = [f"Connections #{puzzle_number}"]
        output_lines.extend(grid_lines)

        return '\n'.join(output_lines)

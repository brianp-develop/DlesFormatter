"""
Base class for puzzle formatters.

All puzzle formatters must inherit from BasePuzzleFormatter and implement
the required methods for detection, parsing, and formatting.
"""

from abc import ABC, abstractmethod
from typing import Optional
import re


class BasePuzzleFormatter(ABC):
    """
    Abstract base class that defines the interface for all puzzle formatters.

    Each puzzle type (Wordle, Framed, etc.) should create a concrete implementation
    that inherits from this class.

    Attributes:
        puzzle_name (str): Unique identifier for this puzzle type (e.g., "wordle")
        detection_pattern (str): Regex pattern to identify this puzzle in input text
    """

    puzzle_name: str = ""
    detection_pattern: str = ""

    @abstractmethod
    def can_parse(self, text: str) -> bool:
        """
        Determine if this formatter can handle the given text.

        Args:
            text: Input text that might contain this puzzle's results

        Returns:
            True if this formatter recognizes the text, False otherwise
        """
        pass

    @abstractmethod
    def parse(self, text: str) -> Optional[dict]:
        """
        Extract puzzle data from the input text.

        Args:
            text: Input text containing puzzle results

        Returns:
            Dictionary containing parsed puzzle data, or None if parsing fails
            Dictionary should include at minimum:
                - 'raw_text': The original text
                - Any other fields needed for formatting
        """
        pass

    @abstractmethod
    def format(self, puzzle_data: dict) -> str:
        """
        Format the parsed puzzle data according to this puzzle's rules.

        Args:
            puzzle_data: Dictionary returned by parse() method

        Returns:
            Formatted string ready for output
        """
        pass

    def process(self, text: str) -> Optional[str]:
        """
        Convenience method that parses and formats in one step.

        Args:
            text: Input text containing puzzle results

        Returns:
            Formatted string, or None if parsing fails
        """
        puzzle_data = self.parse(text)
        if puzzle_data:
            return self.format(puzzle_data)
        return None

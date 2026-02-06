"""
Puzzle Formatters Package

Auto-discovers and registers all puzzle formatter classes.
This registry pattern allows adding new puzzles without modifying core logic.
"""

from .base import BasePuzzleFormatter
from .connections import ConnectionsFormatter
from .framed import FramedFormatter, FramedOneFrameFormatter
from .quolture import QuoltureFormatter
from .strands import StrandsFormatter
from .wordle import WordleFormatter

# Registry of all available formatters
# New formatters are automatically included when imported above
ALL_FORMATTERS = [
    ConnectionsFormatter(),
    FramedFormatter(),
    FramedOneFrameFormatter(),
    QuoltureFormatter(),
    StrandsFormatter(),
    WordleFormatter(),
]


def get_formatter_for_text(text: str):
    """
    Find the appropriate formatter for the given text.

    Tries each registered formatter's can_parse() method until one matches.

    Args:
        text: Input text that might contain puzzle results

    Returns:
        Instance of a formatter that can handle this text, or None if no match
    """
    for formatter in ALL_FORMATTERS:
        if formatter.can_parse(text):
            return formatter
    return None


def get_formatter_by_name(puzzle_name: str):
    """
    Get a formatter by its puzzle_name identifier.

    Args:
        puzzle_name: Unique identifier (e.g., "wordle", "framed_regular")

    Returns:
        Instance of the formatter with matching puzzle_name, or None if not found
    """
    for formatter in ALL_FORMATTERS:
        if formatter.puzzle_name == puzzle_name:
            return formatter
    return None


__all__ = [
    'BasePuzzleFormatter',
    'ConnectionsFormatter',
    'FramedFormatter',
    'FramedOneFrameFormatter',
    'QuoltureFormatter',
    'StrandsFormatter',
    'WordleFormatter',
    'ALL_FORMATTERS',
    'get_formatter_for_text',
    'get_formatter_by_name',
]

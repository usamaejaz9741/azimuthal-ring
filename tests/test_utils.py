"""Tests for the utils.py module.

This module contains unit tests for the utility functions.
"""

from utils import format_time, get_help_text


def test_format_time_valid():
    """Test format_time with a valid ISO timestamp.

    Args:
        None

    Returns:
        None
    """
    ts = "2023-10-27T10:00:00"
    assert format_time(ts) == "2023-10-27 10:00"

def test_format_time_invalid():
    """Test format_time with an invalid timestamp string.

    Args:
        None

    Returns:
        None
    """
    ts = "not-a-timestamp"
    assert format_time(ts) == "not-a-timestamp"

def test_get_help_text():
    """Test the get_help_text function.

    Args:
        None

    Returns:
        None
    """
    help_text = get_help_text()
    assert "Local Assistant Help" in help_text
    assert "/note" in help_text
    assert "/task" in help_text
    assert "/remind" in help_text

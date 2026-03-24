"""Tests for the search.py module.

This module contains unit tests for the web search functionality.
"""

import pytest
from unittest.mock import MagicMock, patch
from search import quick_search


def test_quick_search_success():
    """Test quick_search when it successfully retrieves results."""
    with patch('search.DDGS') as mock_ddgs:
        mock_instance = MagicMock()
        mock_ddgs.return_value.__enter__.return_value = mock_instance
        mock_instance.text.return_value = [
            {'title': 'Title 1', 'body': 'Body 1'},
            {'title': 'Title 2', 'body': 'Body 2'}
        ]

        result = quick_search("test query")
        assert "Title 1: Body 1" in result
        assert "Title 2: Body 2" in result

def test_quick_search_no_results():
    """Test quick_search when no results are found."""
    with patch('search.DDGS') as mock_ddgs:
        mock_instance = MagicMock()
        mock_ddgs.return_value.__enter__.return_value = mock_instance
        mock_instance.text.return_value = []

        result = quick_search("test query")
        assert result == "No results found."

def test_quick_search_error():
    """Test quick_search when an error occurs during the search."""
    with patch('search.DDGS') as mock_ddgs:
        mock_instance = MagicMock()
        mock_ddgs.return_value.__enter__.side_effect = Exception("Search API error")

        result = quick_search("test query")
        assert "Search failed: Search API error" in result

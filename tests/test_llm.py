"""Tests for the llm.py module.

This module contains unit tests for the TinyLLM class and its methods.
"""

import pytest
from unittest.mock import MagicMock, patch
import os
from llm import TinyLLM


@pytest.fixture
def mock_llama():
    """Fixture to mock the Llama class from llama_cpp.

    Yields:
        MagicMock: A mocked Llama class.
    """
    with patch('llm.Llama') as mock:
        yield mock

def test_tinyllm_no_model_file(mock_llama):
    """Test TinyLLM behavior when the model file does not exist.

    Args:
        mock_llama: Mocked Llama class.
    """
    with patch('os.path.exists', return_value=False):
        service = TinyLLM()
        service.load_model()
        assert service.model is None
        assert service.generate("hello") == "Note: Local AI is disabled because the model file was not found."

def test_tinyllm_load_error(mock_llama):
    """Test TinyLLM behavior when the model fails to load.

    Args:
        mock_llama: Mocked Llama class.
    """
    mock_llama.side_effect = Exception("Load failed")
    with patch('os.path.exists', return_value=True):
        service = TinyLLM()
        service.load_model()
        assert service.model is None

def test_tinyllm_generate(mock_llama):
    """Test the generate method of TinyLLM.

    Args:
        mock_llama: Mocked Llama class.
    """
    mock_instance = MagicMock()
    mock_llama.return_value = mock_instance
    mock_instance.return_value = {
        'choices': [{'text': 'Hello world'}]
    }

    with patch('os.path.exists', return_value=True):
        service = TinyLLM()
        service.model = mock_instance
        response = service.generate("Hi")
        assert response == "Hello world"
        mock_instance.assert_called_once()

def test_tinyllm_summarize(mock_llama):
    """Test the summarize method of TinyLLM.

    Args:
        mock_llama: Mocked Llama class.
    """
    mock_instance = MagicMock()
    mock_llama.return_value = mock_instance
    mock_instance.return_value = {
        'choices': [{'text': 'Summary'}]
    }

    with patch('os.path.exists', return_value=True):
        service = TinyLLM()
        service.model = mock_instance
        response = service.summarize("Long text")
        assert response == "Summary"

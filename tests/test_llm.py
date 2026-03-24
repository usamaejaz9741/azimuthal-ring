import pytest
from unittest.mock import MagicMock, patch
import os
from llm import TinyLLM

@pytest.fixture
def mock_llama():
    with patch('llm.Llama') as mock:
        yield mock

def test_tinyllm_no_model_file(mock_llama):
    with patch('os.path.exists', return_value=False):
        service = TinyLLM()
        service.load_model()
        assert service.model is None
        assert service.generate("hello") == "Note: Local AI is disabled because the model file was not found."

def test_tinyllm_load_error(mock_llama):
    mock_llama.side_effect = Exception("Load failed")
    with patch('os.path.exists', return_value=True):
        service = TinyLLM()
        service.load_model()
        assert service.model is None

def test_tinyllm_generate(mock_llama):
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

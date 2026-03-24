import os
import importlib
import config
from unittest.mock import patch

def test_authorized_user_id_valid():
    """Test config with a valid integer AUTHORIZED_USER_ID.

    Args:
        None

    Returns:
        None
    """
    with patch.dict(os.environ, {"AUTHORIZED_USER_ID": "12345"}):
        importlib.reload(config)
        assert config.AUTHORIZED_USER_ID == 12345

def test_authorized_user_id_invalid():
    """Test config with an invalid AUTHORIZED_USER_ID string.

    Args:
        None

    Returns:
        None
    """
    with patch.dict(os.environ, {"AUTHORIZED_USER_ID": "not-an-int"}):
        with patch('builtins.print') as mock_print:
            importlib.reload(config)
            assert config.AUTHORIZED_USER_ID is None
            # Check if warning was printed
            mock_print.assert_any_call("Warning: AUTHORIZED_USER_ID must be an integer. Security restriction disabled.")

def test_authorized_user_id_empty():
    """Test config with an empty AUTHORIZED_USER_ID.

    Args:
        None

    Returns:
        None
    """
    # When it's empty string or whitespace, the 'if AUTHORIZED_USER_ID and AUTHORIZED_USER_ID.strip():'
    # check fails, and the original value (from os.getenv) is kept.
    with patch.dict(os.environ, {"AUTHORIZED_USER_ID": "  "}):
        importlib.reload(config)
        assert config.AUTHORIZED_USER_ID == "  "

def test_authorized_user_id_unset():
    """Test config when AUTHORIZED_USER_ID is not set.

    Args:
        None

    Returns:
        None
    """
    if "AUTHORIZED_USER_ID" in os.environ:
        del os.environ["AUTHORIZED_USER_ID"]
    importlib.reload(config)
    assert config.AUTHORIZED_USER_ID is None

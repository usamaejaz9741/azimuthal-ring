from utils import format_time, get_help_text

def test_format_time_valid():
    ts = "2023-10-27T10:00:00"
    assert format_time(ts) == "2023-10-27 10:00"

def test_format_time_invalid():
    ts = "not-a-timestamp"
    assert format_time(ts) == "not-a-timestamp"

def test_get_help_text():
    help_text = get_help_text()
    assert "Local Assistant Help" in help_text
    assert "/note" in help_text
    assert "/task" in help_text
    assert "/remind" in help_text

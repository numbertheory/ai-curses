from ai_curses.config import AiCursesConfig
from ai_curses.handle_messages import initialize
from ai_curses.handle_messages import quit_program
import pytest


def standard_test_config():
    configuration = {
        "timeout": 10,
        "super": "You are not a helpful assistant at all!",
        "output_dir": None,
        "output_md": None,
        "output_json": None,
        "load_history_json": None
    }
    c = AiCursesConfig(configuration)
    return c


def test_initialize():
    test = initialize(standard_test_config())
    assert test
    assert test[0].get('role') == 'system'
    assert test[0].get('content') == 'You are not a helpful assistant at all!'


def test_quit():
    c = standard_test_config()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        quit_program([], c)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

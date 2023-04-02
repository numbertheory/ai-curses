from ai_curses.config import AiCursesConfig
from ai_curses.handle_messages import initialize


def test_initialize():
    configuration = {
        "timeout": 10,
        "super": "You are not a helpful assistant at all!",
        "output_dir": None,
        "output_md": None,
        "output_json": None,
        "load_history_json": None
    }
    c = AiCursesConfig(configuration)
    test = initialize(c)
    assert test
    assert test[0].get('role') == 'system'
    assert test[0].get('content') == 'You are not a helpful assistant at all!'

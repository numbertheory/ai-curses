from ai_curses import api_wrap
from mock import patch, Mock


@patch('requests.post')
def test_api_wrap_post(mocked):
    mocked.return_value = Mock(
        status_code=201,
        json=lambda: [{"response": "tacos"}],
        text='[{"response": "tacos"}]')
    c = api_wrap.post("http://example.com")
    assert isinstance(c.json(), (list))
    assert c.json() == [{"response": "tacos"}]
    assert c.status_code == 201
    assert c.text == '[{"response": "tacos"}]'

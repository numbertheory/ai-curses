from ai_curses import api_wrap
from mock import patch, Mock
import requests


@patch('requests.post')
def test_api_wrap_post(mocked):
    mocked.return_value = Mock(
        status_code=201,
        json=lambda: [{"response": "tacos"}],
        text='[{"response": "tacos"}]')
    c = api_wrap.post(
        "http://example.com",
        timeout=0.0005,
        headers={'SomeHeading': 'SomeValue'},
        body={"some_content": "reply"}
    )
    assert isinstance(c.json(), (list))
    assert c.json() == [{"response": "tacos"}]
    assert c.status_code == 201
    assert c.text == '[{"response": "tacos"}]'


@patch('requests.post')
def test_api_wrap_fallback_connection_error(mocked):
    mocked.side_effect = requests.exceptions.ConnectionError()
    c = api_wrap.post("http://example.com")
    assert c.status_code == 504
    assert c.text == \
        "A connection to the API could not be established. Try again."


@patch('requests.post')
def test_api_wrap_fallback_timeout(mocked):
    mocked.side_effect = requests.exceptions.ReadTimeout()
    c = api_wrap.post("http://example.com", timeout=12)
    assert c.status_code == 408
    assert c.text == "The API timed out after 12 seconds."

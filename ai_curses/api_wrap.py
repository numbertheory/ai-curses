#! /usr/bin/env python3
import requests


class FallBack():
    """ Fallback object for requests to surface API timeouts safely. """
    def __init__(self, text):
        self.status_code = 408
        self.text = text

    def json(self):
        return {"choices": [{"text": "Sorry, your request timed out!",
                             "message": {
                                "content": self.text
                             }}]}


def post(url, **kwargs):
    headers = kwargs.get("headers", {"Content-type": "application/json"})
    body = kwargs.get("body", {})
    timeout_seconds = kwargs.get("timeout", 95)
    try:
        main_request = requests.post(
            url, headers=headers, json=body,
            timeout=(3, timeout_seconds))
    except requests.exceptions.ReadTimeout:
        return FallBack(
            f"The API timed out after {timeout_seconds} seconds."
        )
    except requests.exceptions.ConnectionError:
        return FallBack(
            "A connection to the API could not be established. Try again."
        )
    return main_request

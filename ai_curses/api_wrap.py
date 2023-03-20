#! /usr/bin/env python3
import requests


class FallBack():
    """ Fallback object for requests to surface API timeouts safely. """
    def __init__(self):
        self.status_code = 408

    def json(self):
        return {"choices": [{"text": "Sorry, your request timed out!"}]}


def post(url, **kwargs):
    headers = kwargs.get("headers", {"Content-type": "application/json"})
    body = kwargs.get("body", {})
    try:
        main_request = requests.post(
            url, headers=headers, json=body,
            timeout=(3, 10))
    except requests.exceptions.ReadTimeout:
        return FallBack()
    return main_request

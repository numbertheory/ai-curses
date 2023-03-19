#! /usr/bin/env python3
import requests


def post(url, **kwargs):
    headers = kwargs.get("headers", {"Content-type": "application/json"})
    body = kwargs.get("body", {})
    return requests.post(url, headers=headers, json=body)

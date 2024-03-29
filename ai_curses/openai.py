#! /usr/bin/env python3
import ai_curses.api_wrap as api_wrap
import os


def get_response(query):
    intro = "This is a conversation with a human being. " \
            "Provide the next message that would be said " \
            "as a reply to the last line of text."
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {os.getenv('CHATGPT_TOKEN')}"
    }
    body = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": f"{intro}\n{query}",
        "temperature": 0.68,
        "max_tokens": 2048
    }
    return api_wrap.post("https://api.openai.com/v1/completions",
                         headers=headers,
                         body=body)


def chat(query):
    openai_req = get_response(query)
    if openai_req.status_code == 200 or openai_req.status_code == 408:
        return openai_req.json()['choices'][0]['text'], openai_req.status_code
    else:
        return f"Sorry, your request did not go through: {openai_req.text} ",
        500


def get_chat_reply(messages, **kwargs):
    timeout = int(kwargs.get("timeout", 95))
    model = kwargs.get("model", "gpt-4")
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {os.getenv('CHATGPT_TOKEN')}"
    }
    body = {
        "model": model,
        "messages": messages
    }
    return api_wrap.post("https://api.openai.com/v1/chat/completions",
                         headers=headers,
                         body=body,
                         timeout=timeout)


def get_image(prompt, **kwargs):
    timeout = int(kwargs.get("timeout", 95))
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {os.getenv('CHATGPT_TOKEN')}"
    }
    body = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    return api_wrap.post("https://api.openai.com/v1/images/generations",
                         headers=headers,
                         body=body,
                         timeout=timeout)


def chatgpt(messages, **kwargs):
    timeout = int(kwargs.get("timeout", 95))
    model = kwargs.get("model", "gpt-4")
    openai_req = get_chat_reply(messages, timeout=timeout, model=model)
    error_msg = f"Sorry, your request did not go through: {openai_req.text} "
    if openai_req.status_code == 200 or openai_req.status_code == 408:
        return_val = "\n".join([x['message']['content']
                                for x in openai_req.json()['choices']])
        return return_val, openai_req.status_code
    else:
        return error_msg, 500

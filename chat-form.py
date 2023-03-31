#!/usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import new_prompt
import math
import time


def quit(app):
    exit(0)


def command_prompt(app, request_id):
    return new_prompt.user_prompt(
        app, prompt_x=0, prompt_y=app.rows - 4,
        cursor_x=0, cursor_y=app.rows - 4,
        height=4, width=app.cols,
        request_id=request_id
    )


def set_prompt_title(app, processing=None):
    app.panels["prompt_title"] = app.panel(
        height=3, width=app.cols, y=app.rows - 5, x=0
    )
    if processing:
        app.print("Prompt: Processing ...{}".format(" " * (app.cols - 22)),
                  x=0, y=0, color="black_on_grey", panel="prompt_title.0")
    else:
        app.print("Prompt{}".format(" " * (app.cols - 6)),
                  x=0, y=0, color="black_on_grey", panel="prompt_title.0")


def find_scroll_amount(columns, text):
    if len(text) <= columns:
        return 2
    else:
        return math.ceil(len(text) / columns) + 1


def process_request(command):
    for i in [1, 2, 3, 4, 5]:
        time.sleep(1)
    return command


def dashport(stdscr):
    app = Dashport(stdscr, color_default="red_on_blue")
    app.layout("single_panel", scroll=True)
    app.user_prompt_position = 1
    request_id = 0
    request_count = 1
    while True:
        while True:
            set_prompt_title(app)
            command, request_id = command_prompt(app, request_id)
            if command == "quit" or command == "exit":
                quit(app)
            if request_id == request_count:
                app.panels["prompt"].clear()
                app.screen.refresh()
                set_prompt_title(app, processing=True)
                process_request(command)
                app.print(x=0, y=app.rows - 5, content=f"{command}",
                          panel="layout.0")
                scroll_amount = find_scroll_amount(app.cols, command)
                app.panels["layout"][0].scroll(scroll_amount)
                request_count += 1
    app.refresh()


if __name__ == '__main__':
    wrap(dashport)
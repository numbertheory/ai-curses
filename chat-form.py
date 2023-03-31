#!/usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import new_prompt


def quit(app):
    exit(0)


def dashport(stdscr):
    app = Dashport(stdscr, color_default="red_on_blue")
    app.add_control("q", quit, case_sensitive=False)
    app.layout("single_panel")
    app.user_prompt_position = 1
    request_id = 1
    while True:
        while True:
            command, request_id = new_prompt.user_prompt(
                app, prompt_x=0, prompt_y=app.rows - 4,
                cursor_x=1, cursor_y=app.rows - 4,
                height=4, width=app.cols,
                request_id=request_id) 
            if command == "quit" or command == "exit":
                quit(app)
    app.refresh()


if __name__ == '__main__':
    wrap(dashport)
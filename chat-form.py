#!/usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import new_prompt


def quit(app):
    exit(0)


def command_prompt(app, request_id):
    return new_prompt.user_prompt(
        app, prompt_x=0, prompt_y=app.rows - 4,
        cursor_x=0, cursor_y=app.rows - 4,
        height=4, width=app.cols,
        request_id=request_id
    )


def set_prompt_title(app):
    app.panels["prompt_title"] = app.panel(
        height=3, width=app.cols, y=app.rows - 5, x=0
    )
    app.print("Prompt{}".format(" " * (app.cols - 6)),
              x=0, y=0, color="black_on_grey", panel="prompt_title.0")


def dashport(stdscr):
    app = Dashport(stdscr, color_default="red_on_blue")
    app.layout("single_panel", scroll=True)
    app.user_prompt_position = 1
    request_id = 1
    app.print("This is the first panel in the layout.", x=5, y=2, panel="layout.0")
    while True:
        while True:
            set_prompt_title(app)
            command, request_id = command_prompt(app, request_id)
            if command == "quit" or command == "exit":
                quit(app)
            app.print(x=0, y=app.rows - 5, content=f"{request_id}", panel="layout.0")
            app.panels["layout"][0].scroll(2)
    app.refresh()


if __name__ == '__main__':
    wrap(dashport)
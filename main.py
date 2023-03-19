#! /usr/bin/env python3
from dashport.dash import Dashport
from dashport.run import wrap
from dashport.prompt import user_prompt


def quit():
    exit(0)


def dashport(stdscr):
    app = Dashport(stdscr, color_default=8)
    app.layout("single_panel", border=False, scroll=True, height=app.rows - 1)
    app.commands = []
    while True:
        while True:
            app.user_prompt_position = 1
            app.print(content="{}".format(app.current_command),
                      x=0, y=app.rows - 2, panel="layout.0")
            app.addstr(">", x=0, y=app.rows - 1)
            command = user_prompt(app, x=2, y=app.rows - 1)
            if command == "quit":
                quit()
            else:
                app.panels["layout"][0].scroll(1)
        app.refresh()


if __name__ == '__main__':
    wrap(dashport)

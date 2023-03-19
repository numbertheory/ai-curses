#! /usr/bin/env python3
from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import new_prompt


def quit():
    exit(0)


def ai_response(prompt):
    return f"This was {len(prompt)} character(s) long."


def dashport(stdscr):
    app = Dashport(stdscr, color_default=8)
    app.layout("single_panel", border=False, scroll=True, height=app.rows - 4)
    app.addstr(">", x=0, y=app.rows - 3)
    app.commands = []
    while True:
        while True:
            app.user_prompt_position = 1
            command = new_prompt.user_prompt(app, x=2, y=app.rows - 3,
                                             height=2, width=app.cols)
            response = f"{ai_response(command)}"
            app.print(content="Human> {}".format(app.current_command),
                      x=0, y=app.rows - 3, panel="layout.0")
            app.print(content="AI> {}".format(response),
                      color="green_on_default",
                      x=0, y=app.rows - 2, panel="layout.0")
            app.addstr(">", x=0, y=app.rows - 3)
            
            if command == "quit" or command == "exit":
                quit()
        
        app.refresh()


if __name__ == '__main__':
    wrap(dashport)

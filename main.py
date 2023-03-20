#! /usr/bin/env python3
from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import new_prompt
from ai_curses import openai
import argparse

parser = argparse.ArgumentParser(
                    prog='AI-Curses',
                    description='Interact with AI platforms in a terminal.')
parser.add_argument('-v', '--verbose',
                    help="Show history after each question.",
                    action='store_true')
parser.add_argument('-s', '--size',
                    help="Show history size after each question.",
                    action='store_true')
args = parser.parse_args()


def quit():
    exit(0)


def ai_response(prompt, history):
    full_history = " ".join([f"{x.get('query')}\n{x.get('response')}\n"
                             for x in history])
    msg, status_code = openai.chat(
        f"{full_history}\n{prompt.strip()}"
    )
    if status_code == 200:
        history.append({"query": f"{prompt.strip()}\n",
                        "response": f"{msg}\n"})
    return msg.splitlines(), history


def dashport(stdscr):
    app = Dashport(stdscr, color_default=8)
    app.layout("single_panel", border=False, scroll=True, height=app.rows - 4)
    app.addstr(">", x=0, y=app.rows - 3)
    app.commands = []
    request_id = 0
    request_count = 1
    history = []
    while True:
        while True:
            app.user_prompt_position = 1
            command, request_id = new_prompt.user_prompt(
                app, x=2, y=app.rows - 3,
                height=2, width=app.cols,
                request_id=request_id)
            if command == "quit" or command == "exit":
                quit()
            if request_id == request_count:
                app.panels["prompt"].clear()
                app.print(content="{}".format(command),
                          color="grey_on_default",
                          x=0, y=app.rows - 4, panel="layout.0")
                app.screen.refresh()
                response, history = ai_response(command, history)
                app.print(content="{}".format(" " * len(command)),
                          color="grey_on_default",
                          x=0, y=app.rows - 5, panel="layout.0")
                app.screen.refresh()
                request_count += 1
            app.print(content="Human> {}".format(app.current_command),
                      x=0, y=app.rows - 3, panel="layout.0")
            app.print(content="AI> {}".format("\n".join(response).lstrip()),
                      color="green_on_default",
                      x=0, y=app.rows - 2, panel="layout.0")
            if args.verbose:
                app.print(content="History> {}".format(history),
                          color="red_on_default",
                          x=0, y=app.rows - 2, panel="layout.0")
            if args.size:
                history_size = " ".join(
                    [f"{x.get('query')}\n{x.get('response')}\n"
                     for x in history]
                )
                app.print(content="History> {}".format(len(history_size)),
                          color="red_on_default",
                          x=0, y=app.rows - 2, panel="layout.0")
            app.addstr(">", x=0, y=app.rows - 3)
        app.refresh()


if __name__ == '__main__':
    wrap(dashport)

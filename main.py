#!/usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import config, command_prompt
from ai_curses import handle_messages as hm

args = config.get_config()


def dashport(stdscr):
    app = Dashport(stdscr, color_default="red_on_blue")
    app.layout("single_panel", scroll=True)
    app.user_prompt_position = 1
    request_id = 0
    request_count = 1
    messages = hm.initialize(args)
    while True:
        while True:
            command_prompt.title(app)
            command, request_id = command_prompt.user(app, request_id)
            if command == "quit" or command == "exit":
                hm.quit(app, messages, args)
            if request_id == request_count:
                app.panels["prompt"].clear()
                app.screen.refresh()
                messages.append({"role": "user", "content": command})
                command_prompt.title(app, processing=True)
                hm.process_helper(messages, app, command, args)
                request_count += 1
    app.refresh()


if __name__ == '__main__':
    wrap(dashport)

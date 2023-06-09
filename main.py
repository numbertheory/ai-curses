#!/usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import config, command_prompt
from ai_curses import handle_messages as hm
from ai_curses import meta_commands as mc

args = config.get_config()


def dashport(stdscr):
    app = Dashport(stdscr, color_default="red_on_blue")
    app.layout("single_panel", scroll=True)
    app.user_prompt_position = 1
    request_id = 0
    request_count = 1
    messages = hm.initialize(args)
    hm.show_meta_help(app)
    while True:
        while True:
            command_prompt.title(app)
            command, request_id = command_prompt.user(app, request_id)
            if command == "quit" or command == "exit":
                hm.quit_program(messages, args)
            elif command == ":forget":
                messages.pop(1)
            elif command.startswith(":"):
                mc.handler(app, args, command, messages)
                request_count += 1
            else:
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

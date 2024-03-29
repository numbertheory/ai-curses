#! /usr/bin/env python3
from curses.textpad import Textbox
import curses
import platform


def user_prompt(app, **kwargs):
    command_line_entered = []
    cursor_x = kwargs.get("cursor_x", 0)
    cursor_y = kwargs.get("cursor_y", 0)
    prompt_x = kwargs.get("prompt_x", 0)
    prompt_y = kwargs.get("prompt_y", 0)
    request_id = kwargs.get("request_id")

    def backspace_key():
        if platform.system().lower() == "linux":
            return 263
        else:
            return 127


    def validate_text(x):
        invalid_chars = [127, 260, 261, 10]
        if x == 260 and app.user_prompt_position != 0:
            app.user_prompt_position -= 1
        if x == 261:
            app.user_prompt_position += 1
        if x not in invalid_chars and curses.ascii.isprint(x):
            command_line_entered.insert(app.user_prompt_position, chr(x))
            app.user_prompt_position += 1
        if x == backspace_key() and len(command_line_entered) > 0:
            try:
                command_line_entered.pop(len(command_line_entered) - 1)
            except IndexError:
                pass
            app.user_prompt_position -= 1
        app.screen.refresh()
        if x == 127:
            x = 263
        if x == 262:
            x = 1
        if x == 260:
            x = 2
        if x == 261:
            x = 6
        if x == 10:
            x = 7
        if x == 1:
            app.user_prompt_position = 0
        app.current_command = "".join(command_line_entered)
        return x

    if not app.panels.get("prompt"):
        win1, panel1 = app.panel(height=kwargs.get("height", 1),
                                 width=kwargs.get("width", 20),
                                 y=prompt_y,
                                 x=prompt_x)
        app.panels["prompt"] = [win1, panel1]
        app.panel_coords.append([0, 0])
    app.screen.move(cursor_y, cursor_x)
    curses.panel.update_panels()
    app.screen.refresh()
    app.screen.move(cursor_y, cursor_x)
    curses.curs_set(True)
    tb = Textbox(app.panels["prompt"][0], insert_mode=True)
    tb.edit(validate_text)
    curses.setsyx(cursor_y, cursor_x + 1)
    try:
        # only here until the new layout works 100%
        app.panels["prompt"].clear()
    except AttributeError:
        app.panels["prompt"][0].clear()
    request_id += 1
    return app.current_command, request_id

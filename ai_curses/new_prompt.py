#! /usr/bin/env python3
from curses.textpad import Textbox
import curses


def user_prompt(app, **kwargs):
    command_line_entered = []
    cursor_x = kwargs.get("x", 0)
    cursor_y = kwargs.get("y", 0)

    def validate_text(x):
        invalid_chars = [127, 260, 261, 10]
        if x == 260 and app.user_prompt_position != 0:
            app.user_prompt_position -= 1
        if x == 261:
            app.user_prompt_position += 1
        if x not in invalid_chars and curses.ascii.isprint(x):
            command_line_entered.insert(app.user_prompt_position, chr(x))
            app.user_prompt_position += 1
        if x == 127 and len(command_line_entered) > 0:
            try:
                command_line_entered.pop(app.user_prompt_position - 2)
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
                                 y=cursor_y, x=cursor_x)
        app.panels["prompt"] = [win1, panel1]
        app.panel_coords.append([0, 0])
    app.screen.move(cursor_y, cursor_x)
    curses.panel.update_panels()
    app.screen.refresh()
    app.screen.move(cursor_y, cursor_x)
    tb = Textbox(app.panels["prompt"][0], insert_mode=True)
    curses.curs_set(True)
    tb.edit(validate_text)
    curses.curs_set(False)
    app.panels["prompt"].clear()
    return app.current_command

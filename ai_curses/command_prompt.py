from ai_curses import prompt


def user(app, request_id):
    return prompt.user_prompt(
        app, prompt_x=0, prompt_y=app.rows - 4,
        cursor_x=0, cursor_y=app.rows - 4,
        height=4, width=app.cols,
        request_id=request_id
    )


def title(app, processing=None):
    app.panels["prompt_title"] = app.panel(
        height=3, width=app.cols, y=app.rows - 5, x=0
    )
    if processing:
        app.print("Prompt: Processing ...{}".format(" " * (app.cols - 22)),
                  x=0, y=0, color="black_on_grey", panel="prompt_title.0")
    else:
        app.print("Prompt{}".format(" " * (app.cols - 6)),
                  x=0, y=0, color="black_on_grey", panel="prompt_title.0")

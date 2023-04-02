#!/usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import new_prompt
import json
from ai_curses import openai
from ai_curses import config

args = config.get_config()


def quit(app, messages):
    json_dump_text = json.dumps(messages, indent=4)
    if args.output_dir:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            f.write(json_dump_text)
            f.close()
    if args.load_history_json and args.output_md:
        with open(args.output_md, 'a', encoding='utf-8') as f:
            f.write(
                "\n\n## History\n\n"
                "This history was loaded with the `-l` option.\n\n"
                f"```json{json.dumps(messages, indent=4)}```\n\n")
            f.close()
    exit(0)


def command_prompt(app, request_id):
    return new_prompt.user_prompt(
        app, prompt_x=0, prompt_y=app.rows - 4,
        cursor_x=0, cursor_y=app.rows - 4,
        height=4, width=app.cols,
        request_id=request_id
    )


def set_prompt_title(app, processing=None):
    app.panels["prompt_title"] = app.panel(
        height=3, width=app.cols, y=app.rows - 5, x=0
    )
    if processing:
        app.print("Prompt: Processing ...{}".format(" " * (app.cols - 22)),
                  x=0, y=0, color="black_on_grey", panel="prompt_title.0")
    else:
        app.print("Prompt{}".format(" " * (app.cols - 6)),
                  x=0, y=0, color="black_on_grey", panel="prompt_title.0")


def process_request(messages, timeout):
    return openai.chatgpt(messages, timeout=timeout)


def add_to_chat_output(app, text, color):
    new_line_split = text.split('\n')
    paragraphs = []
    for line in new_line_split:
        if len(line) < app.cols:
            paragraphs.append(line)
        else:
            chunks, chunk_size = len(line), app.cols
            y = [line[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
            for i in range(0, len(y)):
                paragraphs.append(y[i])
    for para in paragraphs:
        chunks, chunk_size = len(para), app.cols
        scroller = [para[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
        for line in scroller:
            app.print(
                x=0,
                y=app.rows - 5,
                content="{}".format(f"{str(line):<{app.cols}}"),
                panel="layout.0",
                color=color
            )
            app.panels["layout"][0].scroll(1)
            app.screen.refresh()


def initialize_messages(
    history=None,
    super_command="You are a helpful assistant."
):
    if not history:
        return [{"role": "system", "content": f"{super_command}"}]
    else:
        with open(history, 'r') as f:
            messages = json.load(f)

        return messages


def initialize_output(super_command):
    if args.output_dir:
        with open(args.output_md, 'a', encoding='utf-8') as f:
            f.write(
                "## Prompt\n\n {} \n\n## Conversation\n\n".format(
                    super_command.replace('"""', '')
                )
            )
            f.close()


def message_handler(messages, response, status_code, output_file):
    while len(messages) > 25:
        messages.pop(1)
    if status_code == 200:
        command = messages[-1].get('content')
        messages.append({"role": "assistant", "content": response.strip()})
        if output_file:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write("Human> {} \n\n".format(command))
                f.write("AI> {} \n\n".format(response))
                f.close()
    return messages


def dashport(stdscr):
    app = Dashport(stdscr, color_default="red_on_blue")
    app.layout("single_panel", scroll=True)
    app.user_prompt_position = 1
    request_id = 0
    request_count = 1
    messages = initialize_messages(
        history=args.load_history_json,
        super_command=args.super
    )
    initialize_output(args.super)
    while True:
        while True:
            set_prompt_title(app)
            command, request_id = command_prompt(app, request_id)
            if command == "quit" or command == "exit":
                quit(app, messages)
            if request_id == request_count:
                app.panels["prompt"].clear()
                app.screen.refresh()
                messages.append({"role": "user", "content": command})
                set_prompt_title(app, processing=True)
                response, status_code = process_request(messages, args.timeout)
                messages = message_handler(
                    messages, response, status_code, args.output_md
                )
                add_to_chat_output(app, f"Human> {command}", "aqua_on_navy")
                add_to_chat_output(app, f"AI> {response}", "black_on_silver")
                request_count += 1
    app.refresh()


if __name__ == '__main__':
    wrap(dashport)

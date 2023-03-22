#! /usr/bin/env python3
from dashport.dash import Dashport
from dashport.run import wrap
from ai_curses import new_prompt
from ai_curses import openai
import argparse
from configparser import ConfigParser
from datetime import datetime

parser = argparse.ArgumentParser(
                    prog='AI-Curses',
                    description='Interact with AI platforms in a terminal.')
parser.add_argument('-v', '--verbose',
                    help="Show history after each question.",
                    action='store_true')
parser.add_argument('-s', '--super',
                    help="Set the system prompt for the chat intialization.",
                    default='You are a helpful assistant.')
parser.add_argument('-t', '--timeout',
                    help="Set the API timeout, default is 95 seconds.",
                    default='95')
parser.add_argument('-o', '--output',
                    help="Set path for output text file to save chat.")
parser.add_argument('-c', '--config',
                    help="Set a path for a config file.",
                    default=None)
args = parser.parse_args()

if args.config:
    config = ConfigParser()
    config.read(args.config)
    timeout = config.get('options', 'timeout')
    super_command = config.get('options', 'super')
    verbose = config.get('options', 'verbose')
    output_file = config.get('options', 'output')
else:
    timeout = int(args.timeout)
    super_command = args.super
    verbose = args.verbose
    output_file = args.output

filename_for_md = datetime.now().strftime("%Y-%m-%d at %I_%M_%p")
output_path = "{}/{}.md".format(output_file, filename_for_md)


def quit():
    exit(0)


def ai_response(messages, timeout):
    return openai.chatgpt(messages, timeout=timeout)


def dashport(stdscr):
    app = Dashport(stdscr, color_default=8)
    app.layout("single_panel", border=False, scroll=True, height=app.rows - 4)
    app.addstr(">", x=0, y=app.rows - 3)
    app.commands = []
    request_id = 0
    request_count = 1
    messages = [{"role": "system", "content": super_command}]
    if output_file:
        with open(output_path, 'w', encoding='utf-8') as f:
            current_date = datetime.now().strftime("%B %d, %Y at %I:%m%p")
            f.write(f"# Chat Record {current_date}\n\n")
            remove_triple_quotes = super_command.replace(
                "\"\"\"", "").replace("\n", "")
            f.write(f"System Prompt:\n\n```\n{remove_triple_quotes}\n```\n\n")
            f.write("#chatgpt\n\n")
            f.close()
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
                messages.append({"role": "user", "content": command})
                # Limit the messages to 25 so it can run indefinitely.
                # The first message is the system message, so we
                # should keep index (0)
                while len(messages) > 25:
                    messages.pop(1)

                response, status_code = ai_response(messages, timeout)
                if status_code == 200:
                    messages.append({
                        "role": "assistant",
                        "content": response.strip()[0:200]
                    })
                    if output_file:
                        with open(output_path, 'a', encoding='utf-8') as f:
                            f.write("Human> {} \n\n".format(command))
                            f.write("AI> {} \n\n".format(response))
                            f.close()
                else:
                    # drop the last message if the response was not good
                    messages.pop(len(messages) - 1)
                app.print(content="{}".format(" " * len(command)),
                          color="grey_on_default",
                          x=0, y=app.rows - 5, panel="layout.0")
                app.screen.refresh()
                request_count += 1
            app.print(content="Human> {}".format(app.current_command),
                      x=0, y=app.rows - 3, panel="layout.0")
            app.print(content="AI> {}".format(response),
                      color="green_on_default",
                      x=0, y=app.rows - 2, panel="layout.0")
            if verbose:
                app.print(content="History> {}".format(messages),
                          color="red_on_default",
                          x=0, y=app.rows - 2, panel="layout.0")
            app.addstr(">", x=0, y=app.rows - 3)
        app.refresh()


if __name__ == '__main__':
    wrap(dashport)

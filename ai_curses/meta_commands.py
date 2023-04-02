from ai_curses import handle_messages as hm


def blank_line():
    return " \n"


def help(app, args, command, messages):
    return f"""
{blank_line()}
:help - Show this help.
:history - Show current history stats.
:settings - Show the current settings of this session.
{blank_line()}
Type 'quit' or 'exit' to exit the program.
{blank_line()}
"""


def settings(app, args, command, messages):
    if not args.output_md:
        output_md = "none output file set"
    if not args.output_json:
        output_json = "no output json file set"
    return f"""
{blank_line()}
Settings:
{blank_line()}
Prompt - "{args.super}"
Output Markdown File - {output_md}
Output JSON file - {output_json}
Timeout - {args.timeout} seconds
{blank_line()}
"""


def history(app, args, command, messages):
    role_counts = {"system": 0, "assistant": 0, "user": 0, "unknown": 0}
    for msg in messages:
        role_counts[msg.get('role', 'unknown')] += 1
    return f"""
{blank_line()}
History:
{blank_line()}
# of messages - {len(messages)}
   - system: {role_counts.get('system')}
   - assistant: {role_counts.get('assistant')}
   - user: {role_counts.get('user')}
   - unknown: {role_counts.get('unknown')}
{blank_line()}
"""


def help_menu():
    return {
        "help": help,
        "history": history,
        "settings": settings
    }


def handler(app, args, command, messages):
    meta_command = command.split(":")[1]
    if help_menu().get(meta_command, None):
        hm.add_to_chat_output(
            app, help_menu().get(meta_command, lambda: 'Invalid')(
                app, args, command, messages
            ),
            "green_on_black"
        )
    else:
        hm.add_to_chat_output(
            app,
            f"{blank_line()}You tried a meta-command called "
            f"\"{meta_command}\".\n"
            f"{blank_line()}Unfortunately, I don't know that "
            f"one!\n{blank_line()}",
            "green_on_black"
        )

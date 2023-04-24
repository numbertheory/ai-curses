import argparse
from configparser import ConfigParser
from datetime import datetime


class AiCursesConfig():
    def __init__(self, parsed_config):
        self.timeout = parsed_config.get('timeout')
        self.super = parsed_config.get('super')
        self.output_dir = parsed_config.get('output_dir')
        self.output_md = parsed_config.get('output_md')
        self.output_json = parsed_config.get('output_json')
        self.load_history_json = parsed_config.get('load_history_json')
        self.model = parsed_config.get('model')


def get_config():
    parser = argparse.ArgumentParser(
        prog='./main.py',
        description='Interact with AI platforms in a terminal.'
    )
    parser.add_argument(
        '-s', '--super',
        help="Set the system prompt for the chat intialization.",
        default='You are a helpful assistant.'
    )
    parser.add_argument(
        '-t', '--timeout',
        help="Set the API timeout, default is 95 seconds.",
        default='95')
    parser.add_argument(
        '-o', '--output',
        help="Set path for output text file and JSON quicksave"
              "file to save chat and place on exit.")
    parser.add_argument(
        '-c', '--config',
        help="Set a path for a config file.",
        default=None)
    parser.add_argument(
        '-l', '--load-quicksave',
        help="Load a quicksave JSON file.",
        default=None)
    parser.add_argument(
        '-m', '--model',
        help="Define the model to use, defaults to gpt-4.",
        default="gpt-4")
    args = parser.parse_args()

    if args.config:
        config = ConfigParser()
        config.read(args.config)
        timeout = config.get('options', 'timeout')
        super_command = config.get('options', 'super').replace("\\n", "\n")
        output_file = config.get('options', 'output')
        model = config.get('options', 'model')
    else:
        timeout = int(args.timeout)
        super_command = args.super
        output_file = args.output
        model = args.model

    if args.load_quicksave:
        quicksave_file = args.load_quicksave
    else:
        quicksave_file = None
    filename_for_md = datetime.now().strftime("%Y-%m-%d at %H_%M_%S_%f_%p")
    if output_file:
        output_path = "{}/{}.md".format(output_file, filename_for_md)
        json_path = "{}/{}.json".format(output_file, filename_for_md)
        print(f"Transcript: \"{output_path}\"\nJSON: \"{json_path}\"")
    else:
        output_path = None
        json_path = None

    parsed_config = {
        "timeout": timeout,
        "super": super_command,
        "output_dir": output_file,
        "output_md": output_path,
        "output_json": json_path,
        "load_history_json": quicksave_file,
        "model": model
    }

    return AiCursesConfig(parsed_config)

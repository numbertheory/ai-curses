# ai-curses

This is a general wrapper for AI chat services, like OpenAI's chat GPT. In the future this may cover others.

## Installation

Use pyenv, or set a virtual environment up with python 3.11. Then install poetry, and install the rest of the requirements with:

```
poetry install
```

## Running

To run, use `main-chat.py`, that uses the far more functional chat API that OpenAI is using. The `main.py` file is an implementation using OpenAI's `text-davinci-003` model, which is fine for single chat completion tasks, but has stability issues once the conversation gets too long. The requests for the `/v1/chat/completions` endpoint make it easier to manage the conversation length and how much content is being pushed in each request.

```
python main-chat.py [OPTIONS]
```

To see help, run:

```
python main-chat.py -h
```

## Sample Config

The `-c` or `--config` flag points to an INI config file so that you can set options without having large amounts of flags or text in your command.  This flag is only available for `main-chat.py` at the moment.

This is a sample INI file. The `output` option should be a full absolute path to a directory, the actual filename will be generated based on the system time and date.

```
[options]
timeout = 60
super = "You are an AI chat having a conversation with a human."
verbose = false
output = /home/user/somedir
```

### Options

**timeout**: The time, in seconds, the program will wait for a response from the API. Default: 95 seconds.
**super**: The system prompt that is always the first message in the list of messages sent to the API. Use this to set up a more precise use case, that will be an assumption that the AI will use for all your other messages. Default: "You are a helpful assistant."
**verbose**: Set this to see the exact Python list that is getting sent with each message. Useful for debugging, does not show up in output text file (see option below). Default: false
**output**: Set a directory on your local system to save the output. Default: Not set, no output file is generated.
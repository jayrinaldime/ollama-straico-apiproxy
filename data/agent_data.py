from pathlib import Path
from json import dump, load

directory = Path("./data/agent/")
if not directory.exists():
    directory.mkdir(parents=True)


def chat_settings_write(agent_id, chat_settings):
    agent_file = directory / f"{agent_id}_chat_settings.json"
    with agent_file.open("w", encoding="utf-8") as writer:
        dump(chat_settings, writer)


def chat_settings_read(agent_id):
    agent_file = directory / f"{agent_id}_chat_settings.json"
    if not agent_file.exists():
        return {}
    with agent_file.open("r", encoding="utf-8") as reader:
        chat_settings = load(reader)
        return chat_settings

import json

from pydantic import FilePath
from typing import Any, Dict

from settings import settings

def __get_file_path(filepath: str) -> FilePath:
    return FilePath(f'{settings.data_path}/{filepath}')

def __get_playbook_path(playbook_name: str) -> FilePath:
    playbook_path = f"playbooks/{playbook_name}.json"
    return FilePath(__get_file_path(playbook_path))

def get_playbook_context(playbook_name: str) -> Dict[str, Any]:
    base_path = __get_file_path(f'{settings.base_json_name}')
    playbook_path = __get_playbook_path(playbook_name)

    with open(base_path, "r") as base_file:
        base_context = json.load(base_file)
    with open(playbook_path, "r") as playbook_file:
        playbook_context = json.load(playbook_file)

    return {**base_context, **playbook_context}
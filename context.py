import json

import constants

from functools import cache
from pydantic import FilePath
from typing import Any, Dict

from settings import settings

def __get_file_path(filepath: str) -> FilePath:
    return FilePath(f'{settings.data_path}/{filepath}')


def __get_playbook_path(playbook_name: str) -> FilePath:
    playbook_path = f"playbooks/{playbook_name}.json"
    return FilePath(__get_file_path(playbook_path))

def __get_json_content(filepath: FilePath) -> Dict[str, Any]:
    if not filepath.is_file():
        return {}
    with open(filepath, "r") as file:
        try:
            return json.load(file)
        except Exception:
            return {}


def get_playbook_context(playbook_name: str) -> Dict[str, Any]:
    base_path = __get_file_path(f'{settings.base_json_name}')
    playbook_path = __get_playbook_path(playbook_name)

    base_context = __get_json_content(base_path)
    playbook_context = __get_json_content(playbook_path)

    return {**base_context, **playbook_context}

@cache
def _get_main_page_context(_ttl_hash: int) -> Dict[str, Dict]:
    result = {}
    for playbook_name in constants.playbook_names:
        playbook_data = get_playbook_context(playbook_name)
        result[playbook_data['id']] = {
            'name': playbook_data.get('name'),
            'short_description': playbook_data.get('short_description', constants.no_desciption),

        }
    return {"data": result}

def get_main_page_context() -> Dict[str, Dict]:
    return _get_main_page_context(_ttl_hash=settings.main_page_cache_ttl)
import json
from typing import Any

import utils.log as log_man


# module config
_settings_file_dir = './settings/settings.json'


# module state
_settings_object = None


def _init_module():
    global _settings_object

    with open(_settings_file_dir, 'r') as f:
        log_man.add_log('settings.settings.py', 'DEBUG', f"loading settings file: {_settings_file_dir}")
        json_str = f.read()
        
        _settings_object = json.loads(json_str)


def get_settings(key: str):
    return _settings_object[key]


def set_settings(key: str, new_val: Any):
    _settings_object[key] = new_val


def save_settings():
    with open(_settings_file_dir, 'w') as f:
        log_man.add_log('settings.settings.py', 'DEBUG', f"writing new settings to file: {_settings_file_dir}")
        f.write(json.dumps(_settings_object, indent=2))


_init_module()
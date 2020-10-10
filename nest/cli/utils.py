"""
Created by Epic at 10/10/20
"""
from pathlib import Path


def is_there_a_project_here(directory: Path):
    nest_config = directory / "nest.json"
    return nest_config.is_file()


def is_module_already_added(modules: list, name: str, author: str):
    for module in modules:
        if module["name"] == name and module["author"] == "author":
            return True
    return False

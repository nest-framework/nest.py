"""
Created by Epic at 10/10/20
"""
from nest.cli.utils import is_there_a_project_here, is_module_already_added
from nest.cli.exceptions import NoProjectFound, ModuleAlreadyAdded

from pathlib import Path
from ujson import load, dump


def add(directory: Path, name: str, author: str, *, uri: str = None, download_type: str = "git", version: str):
    if not is_there_a_project_here(directory):
        raise NoProjectFound

    project_file = directory / "nest.json"
    with project_file.open() as f:
        project_config = load(f)

    modules = project_config["modules"]
    if is_module_already_added(modules, name, author):
        raise ModuleAlreadyAdded
    modules.append({
        "name": name,
        "author": author,
        "version": version,
        "type": download_type,
        "download": {
            "uri": uri,
            "type": download_type
        }
    })
    project_config["modules"] = modules
    with project_file.open("w+") as f:
        dump(project_config, f, indent=4)


"""
Created by Epic at 10/9/20
"""
from pathlib import Path
from shutil import rmtree
from ujson import dump


class ProjectAlreadyCreated(Exception):
    def __init__(self):
        super().__init__("There is already a project in this directory!")


def init(directory: Path, *, name: str, version: str, token: str):
    nest_project_file = directory / "nest.json"
    nest_modules_folder = directory / "nest_modules"
    nest_config_file = directory / "nest-secrets.json"
    if nest_project_file.is_file():
        raise ProjectAlreadyCreated
    if nest_modules_folder.is_dir():
        rmtree(str(nest_modules_folder))

    with nest_project_file.open("w+") as f:
        nest_project = {
            "bot_name": name,
            "version": version,
            "modules": []
        }
        dump(nest_project, f, indent=4)
    with nest_config_file.open("w+") as f:
        nest_config = {}
        dump(nest_config, f, indent=4)
    nest_modules_folder.mkdir()

"""
Created by Epic at 10/10/20
"""

from pathlib import Path
from ujson import dump

module_comment = """
\"\"\"
Welcome to your brand new nest module!
Have fun and good luck :)
\"\"\"
class Cog:
    def __init__(self, bot, command_handler):
        self.bot = bot
        self.command_handler = command_handler
        pass
def setup(bot, command_handler):
    Cog(bot, command_handler)
""".strip("\n")


def setup_workspace(directory: Path, version: str):
    nest_module_config = directory / "nest_module.json"
    requirements = directory / "requirements.txt"
    module_script = directory / "module.py"

    with nest_module_config.open("w+") as f:
        module_config = {
            "entrypoint": "module.py",
            "version": version
        }
        dump(module_config, f, indent=4)

    with requirements.open("w+") as f:
        f.write("nest.py\nspeedcord")
    with module_script.open("w+") as f:
        f.write(module_comment)


"""
Created by Epic at 10/11/20
"""
from nest.cli.utils import get_file_contents, warn, is_there_a_project_here, clear_logs
from nest.cli.exceptions import NoProjectFound

from pathlib import Path
from tqdm import tqdm
from ujson import loads, load
from aiohttp import ClientSession
from asyncio import Event, create_subprocess_shell, Lock, get_event_loop
from sys import executable

session = ClientSession()
session.headers = {
    "User-Agent": "Nest.py (https://github.com/nest-framework/nest.py)"
}

write_lock = Lock()


async def install(directory: Path):
    nest_config_file = directory / "nest.json"

    if not is_there_a_project_here(directory):
        raise NoProjectFound
    with nest_config_file.open() as f:
        project = load(f)

    loop = get_event_loop()
    events = []

    await write_lock.acquire()
    for module in project["modules"]:
        event = Event()
        events.append(event)
        loop.create_task(install_module(directory, module, event=event))

    for event in tqdm(events, desc="Install dependencies"):
        await event.wait()

    clear_logs()
    write_lock.release()


async def install_module(directory: Path, module: dict, *, event: Event):
    file_contents = await get_file_contents(session, user=module["author"], name=module["name"],
                                            file_name="nest-config.json")
    if file_contents is None:
        warn(f"Failed to install module {module['download']['uri']}. Reason: No nest-module.json config.")
        event.set()
        return
    module_config = loads(file_contents)
    requirements_text = await get_file_contents(session, module["author"], module["name"], "requirements.txt")
    if requirements_text is None:
        requirements = []
    else:
        requirements = requirements_text.replace("\n", " ")
    if not any([requirement.lower().startswith("nest.py") for requirement in requirements]):
        warn(f"Failed to install module {module['uri']}. "
             f"Reason: nest.py is not in the requirements.txt file, please add it to the requirements.txt file.")
        event.set()
        return
    await create_subprocess_shell(f"{executable} -m pip install {requirements}")
    entry_point = module_config["entrypoint"]

    module_folder = directory / "nest_modules"
    author_folder = module_folder / module["author"]
    module_file = author_folder / module["name"]

    if not author_folder.is_dir():
        author_folder.mkdir()

    with module_file.open("w+") as f:
        module_code = await get_file_contents(session, module["author"], module["name"], entry_point)
        f.write(module_code)
    event.set()
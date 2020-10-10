"""
Created by Epic at 10/10/20
"""
from nest.cli.utils import is_there_a_project_here, is_module_already_added, get_uri_data, get_file_contents, warn, \
    clear_logs
from nest.cli.exceptions import NoProjectFound, ModuleAlreadyAdded

from pathlib import Path
from ujson import load, dump, loads
from aiohttp import ClientSession
from asyncio import Lock, get_event_loop, Event
from tqdm import tqdm

session = ClientSession()
session.headers = {
    "User-Agent": "Nest.py (https://github.com/nest-framework/nest.py)"
}

write_lock = Lock()
add_package_lock = Lock()
project = {}
packages = []


async def add_dependencies(*uris, **kwargs):
    global project, packages
    directory: Path = kwargs["directory"]
    nest_config_file = directory / "nest.json"

    if not is_there_a_project_here(directory):
        raise NoProjectFound

    with nest_config_file.open() as f:
        project = load(f)

    loop = get_event_loop()
    events = []

    await write_lock.acquire()
    for uri in uris:
        event = Event()
        events.append(event)
        loop.create_task(add_package(uri, event=event))

    for event in tqdm(events, desc="Add dependencies"):
        await event.wait()

    project["modules"] = packages
    with nest_config_file.open("w") as f:
        dump(project, f, indents=4)

    clear_logs()
    write_lock.release()


async def add_package(uri: str, *, is_dependency=False, event: Event = None):
    print(uri)
    uri_data = get_uri_data(uri)

    if uri_data["download_type"] == "github":
        module_config_text = await get_file_contents(session, uri_data["author"], uri_data["name"], "nest-module.json")
        if module_config_text is None:
            warn(f"Failed to add module {uri}. Reason: No nest-module.json config.")
            if event:
                event.set()
            return
        module_config = loads(module_config_text)
        dependencies = module_config["dependencies"]

        requirements_text = await get_file_contents(session, uri_data["author"], uri_data["name"], "requirements.txt")
        if requirements_text is None:
            requirements = []
        else:
            requirements = loads(requirements_text)
        if not any([requirement.lower().startswith("nest.py") for requirement in requirements]):
            warn(f"Failed to add module {uri}. "
                 f"Reason: nest.py is not in the requirements.txt file, please add it to the requirements.txt file.")
            if event:
                event.set()
            return
    else:
        dependencies = []
        requirements = []

    async with add_package_lock:
        packages.append({
            "name": uri_data["name"],
            "author": uri_data["author"],
            "version": uri_data["version"],
            "download": {
                "uri": uri,
                "type": uri_data["download_type"]
            },
            "dependency": {
                "is_dependency": is_dependency,
                "dependencies": dependencies,
                "requirements": requirements,
            }
        })
    loop = get_event_loop()
    events = []
    for dependency in dependencies:
        event = Event()
        events.append(event)
        loop.create_task(add_package(dependency, is_dependency=True, event=event))

    for event in tqdm(events, desc=f"Add dependencies for {uri}"):
        await event.wait()
    if event:
        event.set()

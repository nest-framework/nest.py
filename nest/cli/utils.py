"""
Created by Epic at 10/10/20
"""
from .exceptions import IncorrectModuleFormat

from pathlib import Path
from asyncio import get_event_loop, Future
from aiohttp import ClientSession
from typing import Optional
from re import compile
from colorama import init, Fore, Style

regex = compile("(\w+@)?([A-z0-9-_]+)/([A-z0-9-_]+)(:\d+.\d+.\d+)?")
init()
log_queue = []


def is_there_a_project_here(directory: Path):
    nest_config = directory / "nest.json"
    return nest_config.is_file()


def is_module_already_added(modules: list, name: str, author: str):
    for module in modules:
        if module["name"] == name and module["author"] == "author":
            return True
    return False


class ValuedEvent:
    def __init__(self):
        self.future: Optional[Future] = None
        self.loop = get_event_loop()

    def set(self, value):
        if not self.future.done():
            self.future.set_result(value)

    async def wait(self):
        if self.future.done():
            return self.future.result()
        return await self.future


def get_uri_data(uri: str):
    regex_result = regex.fullmatch(uri)
    if regex_result is None:
        raise IncorrectModuleFormat

    groups = regex_result.groups()
    if groups[0] is None:
        download_type = "github"
    else:
        download_type = groups[0][:-1]

    if groups[3] is None:
        version = None
    else:
        version = groups[3][1:]

    author = groups[1]
    name = groups[2]

    return {
        "uri": uri,
        "name": name,
        "author": author,
        "version": version,
        "download_type": download_type
    }


async def get_file_contents(session: ClientSession, user, name, file_name):
    request = await session.get(f"https://raw.githubusercontent.com/{user}/{name}/master/{file_name}")
    try:
        request.raise_for_status()
    except:
        return None
    return await request.text()


def warn(text):
    log_queue.append(f"[{Fore.YELLOW}WARNING{Style.RESET_ALL}] {text}")


def clear_logs():
    for log in log_queue:
        print(log)

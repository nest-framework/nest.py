"""
Created by Epic at 10/9/20
"""

from nest.cli.commands.init import init
from nest.cli.commands.add import add_dependencies

import click
from pathlib import Path
import re
from asyncio import get_event_loop

regex = re.compile("(\w+@)?(\w+)/(\w+)(:\d+.\d+.\d+)?")


@click.group()
def cli():
    pass


@cli.command(name="init")
@click.option("--directory", default=".")
@click.option("--name", prompt="Bot name")
@click.option("--version", prompt="Version", default="1.0.0")
@click.option("--token", prompt="Bot token")
def init_command(directory, name, version, token):
    current_dir = Path(directory)
    init(current_dir, name=name, version=version, token=token)
    print("Created nest project in current directory!")


@cli.command(name="add")
@click.argument("package")
@click.option("--directory", default=".")
def add_command(package, directory):
    packages = package.split(" ")
    loop = get_event_loop()
    loop.run_until_complete(add_dependencies(*packages, directory=Path(directory)))



def main():
    cli()


if __name__ == "__main__":
    main()

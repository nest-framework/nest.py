"""
Created by Epic at 10/9/20
"""

from nest.cli.commands.init import init
from nest.cli.commands.add import add
from nest.cli.exceptions import IncorrectModuleFormat

import click
from pathlib import Path
import re

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
    current_dir = Path(directory)

    regex_result = regex.fullmatch(package)
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

    add(current_dir, name, author, uri=package, download_type=download_type, version=version)


def main():
    cli()


if __name__ == "__main__":
    main()

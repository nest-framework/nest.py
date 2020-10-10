"""
Created by Epic at 10/9/20
"""

from nest.cli.commands.init import init
from nest.cli.commands.add import add_dependencies
from nest.cli.commands.setup_workspace import setup_workspace
from nest.cli.commands.install import install

import click
from pathlib import Path
from asyncio import get_event_loop
from logging import getLogger, CRITICAL


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


@cli.command(name="setup-workspace")
@click.option("--directory", default=".")
@click.option("--version", default="1.0.0", prompt="Version")
def setup_workspace_command(directory, version):
    setup_workspace(Path(directory), version)


@cli.command(name="install")
@click.option("--directory", default=".")
def install_command(directory):
    loop = get_event_loop()
    loop.run_until_complete(install(Path(directory)))


def main():
    getLogger('asyncio').setLevel(CRITICAL)
    cli()


if __name__ == "__main__":
    main()

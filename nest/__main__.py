"""
Created by Epic at 10/9/20
"""

import click
from pathlib import Path

from nest.cli.commands.init import init


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


def main():
    cli()


if __name__ == "__main__":
    main()

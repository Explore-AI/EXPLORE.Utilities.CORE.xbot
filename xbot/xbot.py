import logging

import click

from xbot_commands.commands import ancestors, config, descendants, ls, search, total


@click.group()
def xbot() -> None:
    """Main CLI entrypoint for xbot."""
    pass


@xbot.group()
def node() -> None:
    """Inspect nodes running in the mesh."""
    pass


@xbot.group()
def port() -> None:
    """Inspect ports on nodes running in the mesh."""
    pass


@xbot.group()
def interface() -> None:
    """Inspect interfaces running in the mesh."""
    pass


xbot.add_command(config)

node.add_command(ls)
node.add_command(total)
node.add_command(search)
node.add_command(descendants)
node.add_command(ancestors)

port.add_command(search)
port.add_command(ls)
port.add_command(total)

interface.add_command(ls)
interface.add_command(total)

if __name__ == "__main__":
    xbot()

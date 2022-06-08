import click

from xbot.commands.commands import ancestors, config, descendants, ls, search, total


@click.group()
def cli() -> None:
    """Main CLI entrypoint for xbot."""
    pass


@cli.group()
def node() -> None:
    """Inspect nodes running in the mesh."""
    pass


@cli.group()
def port() -> None:
    """Inspect ports on nodes running in the mesh."""
    pass


@cli.group()
def interface() -> None:
    """Inspect interfaces running in the mesh."""
    pass


cli.add_command(config)

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

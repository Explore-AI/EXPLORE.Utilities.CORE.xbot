import logging

import click

from xbot_commands.commands import ancestors, create, descendants, ls, search, total

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

logger = logging.getLogger()


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(VALID_LOG_LEVELS),
    default="info",
    help="The desired log level",
)
def xbot(log_level: str) -> None:
    logging.basicConfig(format=FORMATTER, level=getattr(logging, log_level.upper()))
    logger.debug(f"Log level: {log_level.upper()}")


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


node.add_command(ls)
node.add_command(total)
node.add_command(search)
node.add_command(create)
node.add_command(descendants)
node.add_command(ancestors)

port.add_command(search)
port.add_command(ls)
port.add_command(total)

if __name__ == "__main__":
    xbot()

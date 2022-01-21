import click
import sys
import logging
from xbot_commands.util_functions import *

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

logger = logging.getLogger()


@click.command()
@click.option('--count', help='number of items to be listed', type=int)
def ls(count) -> None:
    """ This command lists all the items in the mesh. Example: `xbot node list --5` will list the 5 most recent items.
    """
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    target_data = request_data(base_url)
    if len(target_data) > 0:
        click.echo(
            f"The following {target}s have been provisioned in your mesh: \n")
        for target in target_data[:count]:
            target_name = target["name"]
            logger.info(f"{target_name.upper()}\n")
    else:
        click.echo(f"There are currently no active {target}s in your mesh.")


@click.command()
def total() -> None:
    """ This command lists the total number of items present in the mesh. Example: `xbot node list --total` will list the total number of items in the mesh.
    """
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    target_data = request_data(base_url)
    # print output in red
    logger.info(
        f"The total number of {target}s in your mesh is: {len(target_data)}")

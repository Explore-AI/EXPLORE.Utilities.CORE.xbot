from util_functions import * 

import click
import sys
import logging

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
    """Inspect nodes running in the mesh.
    """
    pass

@xbot.group()
def port() -> None:
    """Inspect ports on nodes running in the mesh.
    """
    pass

@xbot.group()
def interface() -> None:
    """Inspect interfaces running in the mesh.
    """
    pass

@click.command()
@click.option('--count', help='number of items to be listed', type=int)
def list(count) -> None:
    """ This command lists all the items in the mesh. Example: `xbot node list --5` will list the 5 most recent items.
    """
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    target_data = request_data(base_url)
    if len(target_data) > 0:
        click.echo(f"The following {target}s have been provisioned in your mesh: \n")
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
    logger.info(f"The total number of {target}s in your mesh is: {len(target_data)}")
    
node.add_command(list)
node.add_command(total)
port.add_command(list)
port.add_command(total)

if __name__ == '__main__':
    xbot()



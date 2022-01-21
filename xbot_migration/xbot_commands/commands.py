import json
import logging
import sys

import click
import requests

from requests.structures import CaseInsensitiveDict

from xbot_commands.util_functions import get_access_token, request_data

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

logger = logging.getLogger()


@click.command()
@click.option("--count", help="number of items to be listed", type=int)
def ls(count) -> None:
    """List items in the mesh. Example: `xbot node ls --5` will list the 5 most recent items.

    Args:
        count ([int]): number of items to be listed. Defaults to all items available.
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
    """This command lists the total number of items present in the mesh. Example: `xbot node list --total` will list the total number of items in the mesh."""
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    target_data = request_data(base_url)
    logger.info(f"The total number of {target}s in your mesh is: {len(target_data)}")


@click.command()
@click.option("--name", help="name of the node you're searching for")
@click.option("--id", help="name of the node you're searching for")
def search(name: str, id: str) -> None:
    """Search for a specific item.

    Args:
        name (str): name of the item you're searching for
        id (str): ID of the item you're searching for
    """
    target_item = sys.argv[1]
    argument = sys.argv[4]
    access_token = get_access_token()
    base_url = f"http://localhost:3000/{target_item}s"
    request_url = f"{base_url}?name=phfts.{argument}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    response = requests.get(request_url, headers=headers)
    node_data = json.loads(response.text)
    print(json.dumps(node_data, indent=4, sort_keys=True))

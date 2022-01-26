import logging
import sys

import click
import requests

from requests.structures import CaseInsensitiveDict
from rich import print
from rich.console import Console

from xbot_commands.util_functions import (
    fetch_lineage,
    get_access_token,
    list_by_item_age,
    list_by_item_state,
    list_by_state_and_age,
    print_lineage,
    print_search,
    request_data,
    search_by_id,
    search_by_name,
    search_by_type,
)

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

ITEM_STATES = ["provisioned", "started", "active", "error", "stopped", "suspended"]
CLOUD_PROVIDERS = ["aws", "azure", "gcp"]
ITEM_TYPES = ["operational", "enrichment"]

logger = logging.getLogger()
console = Console(record=True)


@click.command()
@click.option("--all", "-a", help="list all items", is_flag=True)
@click.option("--count", help="number of items to be listed", type=int)
@click.option("--state", help="list items by state", type=click.Choice(ITEM_STATES))
@click.option(
    "--age", help="list items provisioned within a certain timeframe", type=int
)
@click.option("--verbose", "-v", is_flag=True, help="print more output.")
@click.pass_context
def ls(
    ctx, all: str, state: str, age: int, count: int = 5, verbose: bool = False
) -> None:
    """List items in the mesh. Example: `xbot node ls --5` will list the 5 most recent items.

    Args:
        age (int): number of days search criteria should apply to.
        count (int): number of items to be listed. Defaults to 5 items.
        state (str): list items by state. Defaults to all states available.
        verbose (bool): whether to print the data in JSON format. Defaults to False.
    """
    target_item = sys.argv[1]
    base_url = f"http://localhost:3000/{target_item}s"
    response_data = request_data(base_url)
    if state and age:
        list_by_state_and_age(age, state, count, target_item, verbose)
    elif state:
        list_by_item_state(state, count, target_item, verbose)
    elif age:
        list_by_item_age(age, count, target_item, verbose)
    elif count:
        print_search(response_data[:count], verbose)
    elif all:
        print_search(response_data, verbose)
    else:
        console.print(
            f"Hmm, I'm not sure what you want me to do. Try [bold green]`xbot {target_item} ls --all`[/bold green] to view all {target_item}s, or [bold green]`xbot {target_item} ls --help`[/bold green] for more options."
        )


@click.command()
@click.option("--name", "-n", help="name of the node you're searching for")
@click.option("--id", "-id", help="name of the node you're searching for")
@click.option(
    "--type",
    help="type of the node you're searching for",
    type=click.Choice(ITEM_TYPES),
)
@click.option("--verbose", "-v", is_flag=True, help="print more output.")
@click.pass_context
def search(ctx: object, name: str, id: str, type: str, verbose: bool) -> None:
    """Search for a specific item.

    Args:
        name (str): name of the item you're searching for
        id (str): ID of the item you're searching for
        verbose (bool): whether to print the data in JSON format. Defaults to False.
    """
    target_item = sys.argv[1]
    argument = sys.argv[4]
    if name:
        response_data = search_by_name(target_item, argument)
        print_search(response_data, verbose)
    elif id:
        response_data = search_by_id(target_item, argument)
        print_search(response_data, verbose)
    elif type:
        response_data = search_by_type(target_item, argument)
        print_search(response_data, verbose)


@click.command()
def total() -> None:
    """This command lists the total number of items present in the mesh. Example: `xbot node list --total` will list the total number of items in the mesh."""
    target_item = sys.argv[1]
    base_url = f"http://localhost:3000/{target_item}s"
    response_data = request_data(base_url)
    console.print(
        f"The total number of {target_item}s in your mesh is: [bold red]{len(response_data)} [/bold red]"
        + "\n"
    )


@click.command()
@click.option("--name", "-n", help="name of the item you're creating", type=str)
@click.option("--domain", help="domain of the item you're creating", type=str)
@click.option(
    "--cloud",
    help="cloud provider that the item is hosted on",
    type=click.Choice(CLOUD_PROVIDERS),
)
@click.pass_context
def create(ctx: object, name: str, domain: str, cloud: str) -> None:
    """This command creates a new item in the mesh. Example: `xbot node create --name "my_node" --domain "waste.water" --cloud aws` will create a new node."""
    access_token = get_access_token()
    target_item = sys.argv[1]
    base_url = f"http://localhost:3000/{target_item}s"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.pgrst.object+json"
    headers["Authorization"] = f"Bearer {access_token}"
    headers["Prefer"] = "return=representation"
    data = {
        "name": name,
        "domain": domain,
        "description": "Created by xbot",
        "node_cloud_provider": cloud,
    }

    response_data = requests.post(base_url, headers=headers, data=data)
    if response_data.status_code == 201:
        console.print("[bold green]Node successfully created[/bold green]\n")
        search_by_name(target_item, name)
    else:
        print(
            f"There was an error creating your node. Status code: {response_data.status_code}. Error message:{response_data.json()['message']}"
        )


@click.command()
@click.argument("id", type=str)
@click.option("--tree", is_flag=True, help="print as ancestor tree")
def descendants(id: str, tree: bool = False) -> None:
    """View the descendants of a node.

    Args:
        id (str): Node ID of the node you wish to view ancestors of.

        Example: `xbot node descendants {node_id}`. Hint: If you're uncertain of the ID of a node, use the `xbot node ls` command to find it.
    """
    requested_data = fetch_lineage(id)
    print_lineage(requested_data, id, "descendant", tree)


@click.command()
@click.argument("id", type=str)
@click.option("--tree", is_flag=True, help="print as ancestor tree")
def ancestors(id: str, tree: bool = False) -> None:
    """View the ancestors of a node.

    Args:
        id (str): Node ID of the node you wish to view ancestors of.

        Example: `xbot node ancestors {node_id}`. Hint: If you're uncertain of the ID of a node, use the `xbot node ls` command to find it.
    """

    requested_data = fetch_lineage(id)
    print_lineage(requested_data, id, "ancestor", tree)

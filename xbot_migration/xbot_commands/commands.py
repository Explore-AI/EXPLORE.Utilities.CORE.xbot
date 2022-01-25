import datetime
import json
import logging
import sys

import click
import requests

from requests.structures import CaseInsensitiveDict

from xbot_commands.util_functions import (
    get_access_token,
    list_by_item_age,
    list_by_item_state,
    list_by_state_and_age,
    print_lineage,
    print_search,
    request_data,
    search_by_id,
    search_by_name,
)

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

ITEM_STATES = ["provisioned", "started", "active", "error", "stopped", "suspended"]
CLOUD_PROVIDERS = ["aws", "azure", "gcp"]

logger = logging.getLogger()


@click.command()
@click.option("--count", help="number of items to be listed", type=int)
@click.option("--state", help="list items by state", type=click.Choice(ITEM_STATES))
@click.option(
    "--age", help="list items provisioned within a certain timeframe", type=int
)
@click.pass_context
def ls(ctx, state: str, age: int, count: int = 5) -> None:
    """List items in the mesh. Example: `xbot node ls --5` will list the 5 most recent items.

    Args:
        age (int): number of days search criteria should apply to.
        count (int): number of items to be listed. Defaults to 5 items.
        state (str): list items by state. Defaults to all states available.
    """
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    target_data = request_data(base_url)
    include_count = ctx.params["count"]
    include_state = ctx.params["state"]
    include_age = ctx.params["age"]
    if include_state and include_age:
        list_by_state_and_age(age, state, count, target)
    elif include_state:
        list_by_item_state(state, count, target)
    elif include_age:
        list_by_item_age(age, count, target)
    elif include_count:
        print_search(target_data[:count])
    else:
        print_search(target_data)


@click.command()
@click.option("--name", help="name of the node you're searching for")
@click.option("--id", help="name of the node you're searching for")
@click.pass_context
def search(ctx: object, name: str, id: str) -> None:
    """Search for a specific item.

    Args:
        name (str): name of the item you're searching for
        id (str): ID of the item you're searching for
    """
    target_item = sys.argv[1]
    argument = sys.argv[4]
    if ctx.params["name"] is not None:
        response = search_by_name(target_item, argument)
        print_search(response)
    elif ctx.params["id"] is not None:
        response = search_by_id(target_item, argument)
        print_search(response)


@click.command()
def total() -> None:
    """This command lists the total number of items present in the mesh. Example: `xbot node list --total` will list the total number of items in the mesh."""
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    target_data = request_data(base_url)
    logger.info(f"The total number of {target}s in your mesh is: {len(target_data)}")


@click.command()
@click.option("--name", help="name of the node you're creating", type=str)
@click.option("--domain", help="domain of the node you're creating", type=str)
@click.option("--cloud", help="cloud provider", type=click.Choice(CLOUD_PROVIDERS))
@click.pass_context
def create(ctx: object, name: str, domain: str, cloud: str) -> None:
    """This command creates a new item in the mesh. Example: `xbot node create --name "my_node" --domain "waste.water" --cloud aws` will create a new node."""
    access_token = get_access_token()
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.pgrst.object+json"
    headers["Authorization"] = f"Bearer {access_token}"
    headers["Prefer"] = "return=representation"
    data = {
        "name": ctx.params["name"],
        "domain": ctx.params["domain"],
        "description": "Created by xbot",
        "node_cloud_provider": ctx.params["cloud"],
    }
    response = requests.post(base_url, headers=headers, data=data)
    if response.status_code == 201:
        print("\nSuccess!\n")
        search_by_name(target, ctx.params["name"])
    else:
        print(
            f"There was an error creating your node. Status code: {response.status_code}. Error message:{response.json()['message']}"
        )


@click.command()
@click.argument("id", type=str)
def descendants(id: str) -> None:
    """View the descendants of a node.

    Args:
        id (str): Node ID of the node you wish to view ancestors of.

        Example: `xbot node descendants {node_id}`. Hint: If you're uncertain of the ID of a node, use the `xbot node ls` command to find it.
    """
    request_url = f"http://localhost:3000/ancestor_nodes?root_node_id=eq.{id}"
    requested_data = request_data(request_url)
    print_lineage(requested_data, id, "descendant")


@click.command()
@click.argument("id", type=str)
def ancestors(id: str) -> None:
    """View the ancestors of a node.

    Args:
        id (str): Node ID of the node you wish to view ancestors of.

        Example: `xbot node ancestors {node_id}`. Hint: If you're uncertain of the ID of a node, use the `xbot node ls` command to find it.
    """

    request_url = f"http://localhost:3000/ancestor_nodes?descendant_node_id=eq.{id}"
    requested_data = request_data(request_url)
    print_lineage(requested_data, id, "ancestor")

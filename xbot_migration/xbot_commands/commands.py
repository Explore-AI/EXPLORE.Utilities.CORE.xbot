import datetime
import json
import logging
import sys

import click

from xbot_commands.util_functions import (
    list_by_item_age,
    list_by_item_state,
    list_by_state_and_age,
    print_search,
    request_data,
)

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

ITEM_STATES = ["provisioned", "started", "active", "error", "stopped", "suspended"]

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
def total() -> None:
    """This command lists the total number of items present in the mesh. Example: `xbot node list --total` will list the total number of items in the mesh."""
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    target_data = request_data(base_url)
    logger.info(f"The total number of {target}s in your mesh is: {len(target_data)}")


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
        search_by_name(target_item, argument)
    elif ctx.params["id"] is not None:
        search_by_id(target_item, argument)


def search_by_id(target_item, argument):
    base_url = f"http://localhost:3000/{target_item}s"
    request_url = f"{base_url}?id=eq.{argument}"
    target_data = request_data(request_url)
    print_search(target_data)


def search_by_name(target_item, argument):
    base_url = f"http://localhost:3000/{target_item}s"
    request_url = f"{base_url}?name=phfts.{argument}"
    target_data = request_data(request_url)
    print_search(target_data)

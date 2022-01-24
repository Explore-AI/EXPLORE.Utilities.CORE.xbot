import datetime
import json
import logging
import sys

import click

from xbot_commands.util_functions import (
    get_access_token,
    get_item_age,
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
def ls(ctx, count: int, state: str, age: str) -> None:
    """List items in the mesh. Example: `xbot node ls --5` will list the 5 most recent items.

    Args:
        count (int): number of items to be listed. Defaults to all items available.
        state (str): list items by state. Defaults to all states available.
    """
    target = sys.argv[1]
    base_url = f"http://localhost:3000/{target}s"
    target_data = request_data(base_url)
    include_count = ctx.params["count"]
    include_state = ctx.params["state"]
    include_age = ctx.params["age"]
    if include_count is not None and include_state is None:
        print_search(target_data[:count])
    elif include_state is not None and include_count is None:
        print_search(target_data)
    elif include_count is not None and include_state is not None:
        print_search(target_data[:count])
    elif include_age is not None:
        request_by_item_age(age, target)
    else:
        click.echo(f"No {target}s match your query.")


def request_by_item_age(age, target):
    from_datetime = datetime.datetime.now() - datetime.timedelta(age)
    base_url = f"http://localhost:3000/{target}s"
    request_url = f"{base_url}?select=*&date_created=gte.{from_datetime}"
    target_data = request_data(request_url)
    click.echo(
        f"The following items were provisioned within the last {age} days:" + "\n"
    )
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

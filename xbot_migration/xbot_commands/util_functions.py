import datetime
import json
import logging
import os

import click
import pytz
import requests

from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
from rich import print
from rich.console import Console
from rich.progress import track
from rich.style import Style
from rich.table import Table

load_dotenv()

console = Console()

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

logger = logging.getLogger()


def get_access_token() -> str:
    """Generates an access token required to make requests to the API.

    Returns:
        str: JWT access token that is used in the headers of all requests.
    """
    try:
        user_email = os.getenv("user_email")
        user_password = os.getenv("user_password")
        url = "http://localhost:3000/rpc/login"
        response = requests.post(
            url, json={"email": user_email, "password": user_password}
        )
        if response.status_code == 200:
            token = response.json()["token"]
            return token
        else:
            click.echo(
                "The details entered are incorrect, do you have the required .env file?"
            )
            exit()
    except Exception as e:
        click.echo(e)
        exit()


def request_data(base_url: str) -> object:
    """Requests data from the API.

    Args:
        base_url (str): the URL and query paramaters to be used in the request.

    Returns:
        object: JSON object containing the data requested based on the base_url.
    """
    access_token = get_access_token()
    request_url = f"{base_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    response = requests.get(request_url, headers=headers)
    target_data = json.loads(response.text)
    return target_data


def print_search(target_data: dict) -> None:
    """Prints the data requested from the API.

    Args:
        target_data (object): JSON object containing the data requested based on the base_url.
    """
    table = Table(title="Results")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("State", justify="left", style="magenta", no_wrap=True)
    table.add_column("Age (days)", justify="left", style="green", no_wrap=True)
    table.add_column("ID", justify="left", style="blue", no_wrap=False)
    n = 0
    for item in target_data:
        age = get_item_age(item)
        n += 1
        table.add_row(
            f'{n}. {item["name"]}', f'{item["node_state"]}', f"{age}", f'{item["id"]}'
        )
    console.print(table)


def get_item_age(item: str) -> str:
    """Calculates the age of an item.

    Args:
        item (object): JSON object containing the data requested based on the base_url.

    Returns:
        str: the age of the item.
    """

    date_created = datetime.datetime.strptime(
        item["date_created"], "%Y-%m-%dT%H:%M:%S.%f%z"
    )
    current = datetime.datetime.now().replace(tzinfo=pytz.UTC)
    tz = pytz.timezone("Africa/Johannesburg")
    current_time = current.astimezone(tz)
    item_age = (current_time - date_created).days
    return item_age


def list_by_state_and_age(
    age: int, state: str = "active", count: int = 5, target: str = "node"
):
    """List items based on their state AND age.

    Args:
        age (int): number of days search criteria should apply to.
        state (string): ["provisioned", "started", "active", "error", "stopped", "suspended"]
        count (int): number of items to be listed. Defaults to 5 items.
        target (str): the target item to be listed e.g. node, port or interface. Defaults to node.
    """
    from_datetime = datetime.datetime.now() - datetime.timedelta(age)
    base_url = f"http://localhost:3000/{target}s"
    request_url = f"{base_url}?select=*&date_created=gte.{from_datetime}&{target}_state=eq.{state}"
    target_data = request_data(request_url)
    if target_data:
        print_search(target_data[:count])
    else:
        logger.info(
            f"No {target}s of state '{state}' provisioned within the last {age} days. Please refine your search."
        )


def list_by_item_state(state: str, count: int = 5, target: str = "node"):
    """List items based on their state.

    Args:
        state (string): ["provisioned", "started", "active", "error", "stopped", "suspended"]
        count (int): number of items to be listed. Defaults to 5 items.
        target (str): the target item to be listed e.g. node, port or interface. Defaults to node.
    """
    base_url = f"http://localhost:3000/{target}s"
    request_url = f"{base_url}?select=*&{target}_state=eq.{state}"
    target_data = request_data(request_url)
    if target_data:
        print_search(target_data[:count])
    else:
        logger.info(f"No {target}s with state '{state}' found.")


def list_by_item_age(age: int, count: int, target: str = "node"):
    """List items based on their age.

    Args:
        age (int): number of days search criteria should apply to.
        state (string): ["provisioned", "started", "active", "error", "stopped", "suspended"]
        count (int): number of items to be listed. Defaults to 5 items.
        target (str): the target item to be listed e.g. node, port or interface. Defaults to node.
    """
    from_datetime = datetime.datetime.now() - datetime.timedelta(age)
    base_url = f"http://localhost:3000/{target}s"
    request_url = f"{base_url}?select=*&date_created=gte.{from_datetime}"
    target_data = request_data(request_url)
    if target_data:
        print_search(target_data[:count])
    else:
        logger.info(f"No {target}s provisioned within the last {age} days.")


def search_by_id(target_item, argument):
    base_url = f"http://localhost:3000/{target_item}s"
    request_url = f"{base_url}?id=eq.{argument}"
    target_data = request_data(request_url)
    return target_data


def search_by_name(target_item, argument):
    base_url = f"http://localhost:3000/{target_item}s"
    request_url = f"{base_url}?name=phfts.{argument}"
    target_data = request_data(request_url)
    return target_data


def print_lineage(requested_data: list, id: str, target_lineage: str) -> None:
    node = search_by_id(target_item="node", argument=id)
    node_name = node[0]["name"]
    table = Table(title=f"\{target_lineage} of {node_name} node \n")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Category", justify="left", style="blue", no_wrap=False)
    table.add_column("ID", justify="left", style="magenta", no_wrap=False)
    n = 0
    for item in requested_data:
        n += 1
        table.add_row(
            f'{n}. {item[f"{target_lineage}_node_name"]}',
            f'{item[f"{target_lineage}_node_category"]}',
            f'{item[f"{target_lineage}_node_id"]}',
        )
    console.print(table)

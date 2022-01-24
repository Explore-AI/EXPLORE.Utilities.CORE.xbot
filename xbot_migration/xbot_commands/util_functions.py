import json
import os

import click
import requests

from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
from rich import print
from rich.console import Console
from rich.progress import track
from rich.style import Style
from rich.table import Table

load_dotenv()

base_node_api_url = "http://localhost:3000/nodes"
console = Console()


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


def print_items(target_data: object) -> None:
    """Prints the data requested from the API.

    Args:
        target_data (object): JSON object containing the data requested based on the base_url.
    """
    for item in target_data:
        item_name = item["name"]
        item_state = item["node_state"]
        click.echo(f"{item_name.upper()} - {item_state}")


def print_search(target_data: object) -> None:
    table = Table(title="Search Results")
    table.add_column("Item", justify="left", style="cyan", no_wrap=True)
    table.add_column("State", justify="left", style="magenta", no_wrap=True)
    n = 0
    for item in target_data:
        n += 1
        table.add_row(f'{n}. {item["name"]}', f'{item["node_state"]}')
    console.print(table)

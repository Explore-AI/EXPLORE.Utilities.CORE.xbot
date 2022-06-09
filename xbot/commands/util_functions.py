import datetime
import json
import logging
import os

from stat import S_IREAD, S_IWUSR
from typing import Dict

import click
import pytz
import requests

from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
from rich import print
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

load_dotenv()

console = Console()

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

CONFIG_FILE = "config.json"


logger = logging.getLogger()


def generate_access_token(host: str, email: str, password: str) -> str:
    """Generates an access token required to make requests to the API.

    Returns:
        str: JWT access token that is used in the headers of all requests.
    """
    try:
        url = f"{host}/rpc/login"
        response = requests.post(url, json={"email": email, "password": password})
        if response.status_code == 200:
            token = response.json()["token"]
            return token
        else:
            click.echo(
                "The details entered are incorrect, please run "
                "[bold red]xbot config -e <your_email> -p <your_password>[/bold red] "
                "or contact your account owner for the required permissions."
            )
            logger.info(f"Failed attempt to generate access token for {email}")
            exit()
    except Exception as e:
        click.echo(e)
        exit()


def read_config() -> Dict[str, str]:
    """
    Read config file
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            d = json.load(f)
        return d
    except FileNotFoundError:
        logger.fatal("No config found, please run `xbot config` to create one.")
    exit()


def retrieve_access_token() -> str:
    """
    Retrieve access token used to access api.

    returns:
        str: access token used to access api.
    """
    cfg = read_config()
    return cfg["access_token"]


def retrieve_output_format() -> str:
    """Retrieves the output format from the config file.

    Returns:
        str: the output format.
    """
    cfg = read_config()
    return cfg["output_format"]


def retrieve_host() -> str:
    """
    Retrieve host of api.

    returns:
        str: hostname of API
    """
    cfg = read_config()
    return cfg["host"]


def write_config(host: str, email: str, password: str, json_format: bool) -> None:
    """Store access token used to access API.

    Args:
        email (str): email used to generate access token.
        password (str[): password used to generate access token.
    """
    access_token = generate_access_token(host, email, password)
    output_format = "json" if json_format else "default"

    data = {"host": host, "access_token": access_token, "output_format": output_format}

    try:
        os.chmod(CONFIG_FILE, S_IWUSR | S_IREAD)
        with open(CONFIG_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
    except FileNotFoundError:
        open(CONFIG_FILE, "w")
        os.chmod(CONFIG_FILE, S_IWUSR | S_IREAD)
        with open(CONFIG_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)


def request_data(url: str) -> dict:
    """Requests data from the API.

    Args:
        url (str): the URL and query paramaters to be used in the request.

    Returns:
        list: JSON object containing the data requested based on the url.
    """
    try:
        access_token = retrieve_access_token()
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers)
        return response
    except Exception as e:
        logger.error(e)
        console.print(
            "It looks like you're not logged in. Please run "
            "[bold green]`xbot config`[/bold green] "
            "to make sure you have the required permissions."
        )


def print_search(target_item: str, response: dict, json: bool = False) -> None:
    """Prints the data requested from the API.

    Args:
        response_data (object): JSON object containing the data requested based on
            the url.
        json (bool): whether to print the data in JSON format. Defaults to False.
    """

    if response.status_code == 200:
        response_data = response.json()
        if len(response_data) == 0:
            console.print(
                "Your query returned no results. Please refine your search and try "
                " again."
            )
        else:
            output_format = retrieve_output_format()
            if output_format == "json" or json:
                console.print_json(data=response_data)
            else:
                if target_item == "node":
                    print_node_results(response_data)
                elif target_item == "port":
                    print_port_results(response_data)
                elif target_item == "interface":
                    print_interface_results(response_data)
    else:
        print_error_message()


def print_port_results(response_data: list):
    """Utility function to print node data in a table structure

    Args:
        response_data (list): data returned from the request_data function
    """
    table = Table(title="Results")
    table.add_column("Number", justify="left", style="cyan", no_wrap=True)
    table.add_column("Name", justify="left", style="magenta", no_wrap=True)
    table.add_column("State", justify="left", style="green", no_wrap=True)
    table.add_column("Description", justify="left", style="blue", no_wrap=False)
    table.add_column("Associated node", justify="left", style="cyan", no_wrap=True)
    for item in response_data:
        table.add_row(
            f'{item["port_number"]}',
            f'{item["name"]}',
            f'{item["port_state"]}',
            f'{item["description"]}',
            f'{item["node_id"]}',
        )
    console.print(table)


def print_node_results(response_data: list):
    """Utility function to print port data in a table structure

    Args:
        response_data (list): data returned from the request_data function
    """
    table = Table(title="Results")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("State", justify="left", style="magenta", no_wrap=True)
    table.add_column("Age (days)", justify="left", style="green", no_wrap=True)
    table.add_column("ID", justify="left", style="blue", no_wrap=False)
    n = 0
    for item in response_data:
        age = get_item_age(item)
        n += 1
        table.add_row(
            f'{n}. {item["name"]}',
            f'{item["node_state"]}',
            f"{age}",
            f'{item["id"]}',
        )
    console.print(table)


def print_interface_results(
    response: list, include_schema: bool = False, json: bool = False
):
    """Utility function to print port data in a table structure

    Args:
        response_data (list): data returned from the request_data function
    """
    try:
        response_data = response.json()
    except AttributeError:
        response_data = response
    output_format = retrieve_output_format()
    if output_format == "json" or json:
        console.print_json(data=response_data)
    else:
        table = Table(title="Results")
        table.add_column("Interface ID", justify="left", style="cyan", no_wrap=True)
        table.add_column("Sub scheme", justify="left", style="blue", no_wrap=True)
        table.add_column("Port number", justify="left", style="green", no_wrap=True)
        table.add_column("Node ID", justify="left", style="magenta", no_wrap=True)
        if include_schema:
            table.add_column(
                "Schema definition function",
                justify="left",
                style="magenta",
                no_wrap=False,
            )
        for item in response_data:
            row = [
                f'{item["id"]}',
                f'{item["interface_sub_scheme"]}',
                f'{item["port_number"]}',
                f'{item["node_id"]}',
            ]
            if include_schema:
                row.append(f'{item["schema_definition_function"]}')
            table.add_row(*row)

        console.print(table)
        console.print(
            "\nHint: To view additional output in JSON format, append "
            "[bold cyan]--json[/bold cyan] or [bold cyan]-j[/bold cyan] to "
            "the previous command.\n"
        )


def get_item_age(item: str) -> str:
    """Calculates the age of an item.

    Args:
        item (object): JSON object containing the data requested based on the url.

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
    age: int,
    state: str = "active",
    target_item: str = "node",
    json: bool = False,
):
    """List items based on their state AND age.

    Args:
        age (int): number of days search criteria should apply to.
        state (str): One of :
            ["provisioned", "started", "active", "error", "stopped", "suspended"]
        target_item (str): the target item to be listed e.g. node, port or interface.
            Defaults to node.
    """
    from_datetime = datetime.datetime.now() - datetime.timedelta(age)
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = (
        f"{url}?select=*"
        f"&date_created=gte.{from_datetime}"
        f"&{target_item}_state=eq.{state}"
    )
    response = request_data(url)
    if response:
        return response
    else:
        console.print(
            "We're having some trouble authenticating your profile. Please run "
            "[bold cyan]xbot config -e <your_email> -p <your_password> [/bold cyan] "
            "to login."
        )


def list_by_type_and_age(
    age: int,
    type: str,
    target_item: str = "node",
    json: bool = False,
):
    """List items based on their state AND age.

    Args:
        age (int): number of days search criteria should apply to.
        target_item (str): the target item to be listed e.g. node, port or interface.
            Defaults to node.
    """
    from_datetime = datetime.datetime.now() - datetime.timedelta(age)
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = (
        f"{url}?select=*"
        f"&date_created=gte.{from_datetime}"
        f"&{target_item}_type=eq.{type}"
    )
    response = request_data(url)
    if response:
        return response
    else:
        print_error_message()


def list_by_type_and_state(
    type: str,
    state: str,
    target_item: str = "node",
    json: bool = False,
):
    """List items based on their state AND age.

    Args:
        type (str): the type of node to be listed e.g. operational, digital-twin or
            aggregate.
        state (str): One of:
            ["provisioned", "started", "active", "error", "stopped", "suspended"]
        target_item (str): the target item to be listed e.g. node, port or interface.
            Defaults to node.
    """
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = (
        f"{url}?select=*"
        f"&{target_item}_state=eq.{state}"
        f"&{target_item}_type=eq.{type}"
    )
    response = request_data(url)
    if response:
        return response
    else:
        print_error_message()


def list_by_item_state(state: str, target_item: str = "node", json: bool = False):
    """List items based on their state.

    Args:
        state (str): One of:
            ["provisioned", "started", "active", "error", "stopped", "suspended"]
        target_item (str): the target item to be listed e.g. node, port or interface.
            Defaults to node.
    """
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = f"{url}?select=*&{target_item}_state=eq.{state}"
    response_data = request_data(url)
    if response_data:
        return response_data
    else:
        logger.info(f"No {target_item}s with state '{state}' found.")


def list_by_item_age(age: int, target_item: str = "node", json: bool = False):
    """List items based on their age.

    Args:
        age (int): number of days search criteria should apply to.
        state (str): One of:
            ["provisioned", "started", "active", "error", "stopped", "suspended"]
        target_item (str): the target item to be listed e.g. node, port or interface.
            Defaults to node.
    """
    from_datetime = datetime.datetime.now() - datetime.timedelta(age)
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = f"{url}?select=*&date_created=gte.{from_datetime}"
    response = request_data(url)
    if response:
        return response
    else:
        logger.info(f"No {target_item}s provisioned within the last {age} days.")


def search_by_id(target_item, argument):
    """Search for an item by its ID.

    Args:
        target_item (str): the target item to be listed e.g. node, port or interface.
        argument (str): the ID of the item to be searched for.

    Returns:
        list: a list of items matching the search criteria.
    """
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = f"{url}?id=eq.{argument}"
    response_data = request_data(url)
    return response_data


def search_by_name(target_item: str, argument: str):
    """Search for an item by its ID.

    Args:
        target_item (str): the target item to be listed e.g. node, port or interface.
        argument (str): the name of the item to be searched for.

    Returns:
        list: a list of items matching the search criteria.
    """
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = f"{url}?name=phfts.{argument}"
    response_data = request_data(url)
    return response_data


def search_by_type(target_item: str, argument: str):
    """Search for an item by its ID.

    Args:
        target_item (str): the target item to be listed e.g. node, port or interface.
        argument (str): the type of the item to be searched for.
            One of: ["operational", "enrichment"]

    Returns:
        list: a list of items matching the search criteria.
    """
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = f"{url}?{target_item}_type=eq.{argument}"
    response_data = request_data(url)
    return response_data


def search_by_interface(target_item: str, argument: str):
    """Search for interfaces on a node.

    Args:
        target_item (str): the target item to be listed e.g. node, port or interface.
            Interface in this instance
        argument (str): the node_id of the node you want to see the interfaces for

    Returns:
        list: a list of items matching the search criteria.
    """
    host = retrieve_host()
    url = f"{host}/{target_item}s"
    url = f"{url}?node_id=eq.{argument}"
    response_data = request_data(url)
    return response_data


def fetch_lineage(id: str) -> list:
    """Fetch the ancestors and descendants of an item.

    Args:
        id (str): ID of item you're looking for the lineage of.

    Returns:
        [list]: a list of items matching the search criteria.
    """
    host = retrieve_host()
    url = f"{host}/ancestor_nodes?root_node_id=eq.{id}"
    requested_data = request_data(url)
    return requested_data


def print_lineage(
    response: object,
    id: str,
    target_lineage: str,
    tree: bool = False,
    json: bool = False,
) -> None:
    """Prints the lineage, i.e. ancestors or descendants, of an item.

    Args:
        response_data (list): a list of items matching the search criteria.
        id (str): ID of the item you want to print the lineage for.
        target_lineage (str): ancestor or descendant.
        tree (bool): whether to print the lineage as a tree.
        json (bool): whether to print the lineage in JSON mode.
    """
    if response.status_code == 200:
        response_data = response.json()
        output_format = retrieve_output_format()
        node = search_by_id(target_item="node", argument=id)
        # It is necessary to convert the node data to json before extracting the name.
        node_name = node.json()[0]["name"]
        if output_format == "json" or json:
            console.print_json(data=response_data)
        elif tree:
            tree_items = [node_name]
            tree = Tree(
                (
                    f"\n[bold cyan]{target_lineage.upper()} "
                    f"TREE: {node_name.upper()}[/bold cyan]"
                )
            )
            for item in response_data:
                item_name = item[f"{target_lineage}_node_name"]
                if item_name not in tree_items:
                    tree.add(item_name)
                    tree_items.append(item_name)
            print(tree)
        else:
            table = Table(title=f"{target_lineage.upper()}S: {node_name.upper()} \n")
            table.add_column("Name", justify="left", style="cyan", no_wrap=True)
            table.add_column("Category", justify="left", style="blue", no_wrap=False)
            table.add_column("ID", justify="left", style="magenta", no_wrap=False)
            table_items = [node_name]
            n = 0
            for item in response_data:
                item_name = item[f"{target_lineage}_node_name"]
                if item_name not in table_items:
                    n += 1
                    table.add_row(
                        f'{n}: {item[f"{target_lineage}_node_name"]}',
                        f'{item[f"{target_lineage}_node_category"]}',
                        f'{item[f"{target_lineage}_node_id"]}',
                    )
                    table_items.append(item_name)
            console.print(table)
    else:
        console.print(
            "It looks like your access token has expired. "
            "Please run: "
            "[bold cyan]xbot config -e <your_email> -p <your_password> [/bold cyan] "
            "to generate a new one."
        )


def print_error_message() -> None:
    """Prints an error message with troubleshooting support if an error occurs."""
    console.print(
        """
            Something went wrong. Try these troubleshooting methods:

            1. Run:
                [bold green]xbot config -e <your_email> -p <your_password> [/bold green]
                to ensure your permissions are configuired.
            2. Contact a member of the CORE team at:
                [bold]core-platform@explore-utilities.com[/bold]
            """
    )

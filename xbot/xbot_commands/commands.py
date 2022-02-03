import json
import logging
import os
import sys

import click
import requests

from requests.structures import CaseInsensitiveDict
from rich import print
from rich.console import Console

from xbot_commands.util_functions import (
    fetch_lineage,
    list_by_item_age,
    list_by_item_state,
    list_by_state_and_age,
    print_interface_results,
    print_lineage,
    print_search,
    request_data,
    retrieve_access_token,
    search_by_id,
    search_by_interface,
    search_by_name,
    search_by_type,
    store_access_token,
)

FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]


CLOUD_PROVIDERS = ["aws", "azure", "gcp"]
ITEM_TYPES = ["operational", "digital-twin", "aggregate"]
ITEM_STATES = ["provisioned", "started", "active", "error", "stopped", "suspended"]

logger = logging.getLogger()
console = Console(record=True)


@click.command()
@click.option("--email", "-e", help="Username")
@click.option("--password", "-p", help="Password")
@click.option("--json", is_flag=True, help="Default to output in JSON format")
def config(email: str, password: str, json: bool) -> None:
    """Stores access token and global settings of the user.

    Args:
        email (str): user email
        password (str): user password
    """
    if email and password:
        store_access_token(email, password, json)
        access_token = retrieve_access_token()
        logger.info(f"Storage of access token: {access_token}")
    else:
        email = click.prompt("Email", type=str)
        password = click.prompt("Password", type=str)
        store_access_token(email, password, json)
        access_token = retrieve_access_token()
        logger.info(f"Storage of access token: {access_token}")


@click.command()
@click.option("--all", "-a", help="list all items", is_flag=True)
@click.option("--state", help="list items by state", type=click.Choice(ITEM_STATES))
@click.option(
    "--age", help="list items provisioned within a certain timeframe", type=int
)
@click.option("--interface", help="provide the node_id to view interfaces on that node")
@click.option(
    "--type",
    help="type of the node you're searching for",
    type=click.Choice(ITEM_TYPES),
)
@click.option("--json", "-j", is_flag=True, help="print more output.")
def ls(
    all: str, state: str, age: int, interface: str, type: str, json: bool = False
) -> None:
    """List items in the mesh. Example: `xbot node ls --5` will list the 5 most recent items.

    Args:
        age (int): number of days search criteria should apply to.
        state (str): list items by state. Defaults to all states available.
        interface (str): provide the node_id to view all interfaces on that node
        json (bool): whether to print the data in JSON format. Defaults to False.
    """
    target_item = sys.argv[1]
    paramater = sys.argv[4]
    base_url = f"http://localhost:3000/{target_item}s"
    response = request_data(base_url)
    if target_item == "node" or target_item == "port":
        if response is not None:
            if state and age:
                list_by_state_and_age(age, state, target_item, json)
            elif state:
                list_by_item_state(state, target_item, json)
            elif age:
                list_by_item_age(age, target_item, json)
            elif all:
                print_search(target_item, response, json)
            elif interface:
                response = search_by_interface("interface", paramater)
                print_search("interface", response, json)
            elif type:
                response = search_by_type(target_item, paramater)
                print_search(target_item, response, json)
            else:
                console.print(
                    f"Hmm, I'm not sure what you want me to do. Try [bold green]`xbot {target_item} ls --all`[/bold green] to view all {target_item}s, or [bold green]`xbot {target_item} ls --help`[/bold green] for more options."
                )
        else:
            exit()
    elif target_item == "interface":
        if response is not None:
            print_interface_results(response, json)


@click.command()
@click.option("--name", "-n", help="name of the node you're searching for")
@click.option("--id", "-id", help="name of the node you're searching for")
@click.option("--json", "-j", is_flag=True, help="print more output.")
def search(name: str, id: str, json: bool) -> None:
    """Search for a specific item.

    Args:
        name (str): name of the item you're searching for
        id (str): ID of the item you're searching for
        json (bool): whether to print the data in JSON format. Defaults to False.
    """
    target_item = sys.argv[1]
    argument = sys.argv[4]
    if name:
        response = search_by_name(target_item, argument)
        print_search(target_item, response, json)
    elif id:
        response = search_by_id(target_item, argument)
        print_search(target_item, response, json)


@click.command()
def total() -> None:
    """This command lists the total number of items present in the mesh. Example: `xbot node list --total` will list the total number of items in the mesh."""
    target_item = sys.argv[1]
    base_url = f"http://localhost:3000/{target_item}s"
    response = request_data(base_url)
    response = response.json()
    console.print(
        f"There are [bold red]{len(response)} [/bold red]{target_item}s in your mesh."
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
    access_token = retrieve_access_token()
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

    response = requests.post(base_url, headers=headers, data=data)
    if response.status_code == 201:
        console.print("[bold green]Node successfully created[/bold green]\n")
        search_by_name(target_item, name)
        access_token = retrieve_access_token()
        logger.info(f"Node created by user with token {access_token}. Node ID: {name}")
    else:
        console.print(
            f"There was an error creating your node. [bold red] Details:[/bold red] Status code - {response.status_code}. Message - {response.json()['message']}"
        )


@click.command()
@click.option("--name", "-n", help="name of the item you're creating", type=str)
@click.option("--id", help="domain of the item you're creating", type=str)
@click.pass_context
def destroy(name: str, id: str) -> None:
    """This command destroys a node that is present in your mesh. Example: `xbot node destory --name "my_node" --domain "waste.water" --cloud aws` will create a new node."""
    access_token = retrieve_access_token()
    target_item = sys.argv[1]
    print(target_item)
    if name:
        base_url = f"http://localhost:3000/{target_item}s?name=phfts.{name}"
    elif id:
        base_url = f"http://localhost:3000/{target_item}s?id=eq.{id}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.pgrst.object+json"
    headers["Authorization"] = f"Bearer {access_token}"
    headers["Prefer"] = "return=representation"
    confirm = console.print("Are you sure? y/n")
    if confirm == "y":
        response = requests.delete(base_url, headers=headers)
        if response.status_code == 204:
            console.print("[bold red]Node successfully destroyed[/bold red]\n")
            search_by_name(target_item, name)
            access_token = retrieve_access_token()
            logger.info(f"Node destroyed by user with token {access_token}.")
        else:
            console.print(
                f"There was an error creating your node. [bold red] Details:[/bold red] Status code - {response.status_code}. Message - {response.json()['message']}"
            )
    else:
        console.print("Aborted.")


@click.command()
@click.argument("id", type=str)
@click.option("--tree", is_flag=True, help="print as ancestor tree")
@click.option("--json", "-j", is_flag=True, help="print output in JSON format.")
def descendants(id: str, tree: bool = False, json: bool = False) -> None:
    """View the descendants of a node.

    Args:
        id (str): Node ID of the node you wish to view ancestors of.

        Example: `xbot node descendants {node_id}`. Hint: If you're uncertain of the ID of a node, use the `xbot node ls` command to find it.
    """
    requested_data = fetch_lineage(id)
    print_lineage(requested_data, id, "descendant", tree, json)


@click.command()
@click.argument("id", type=str)
@click.option("--tree", is_flag=True, help="print as ancestor tree")
@click.option("--json", "-j", is_flag=True, help="print output in JSON format.")
def ancestors(id: str, tree: bool = False, json: bool = False) -> None:
    """View the ancestors of a node.

    Args:
        id (str): Node ID of the node you wish to view ancestors of.

        Example: `xbot node ancestors {node_id}`. Hint: If you're uncertain of the ID of a node, use the `xbot node ls` command to find it.
    """

    requested_data = fetch_lineage(id)
    print_lineage(requested_data, id, "ancestor", tree, json=json)

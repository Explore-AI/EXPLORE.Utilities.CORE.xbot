import logging
import sys

import click

from rich.console import Console

from xbot.commands.util_functions import (
    fetch_lineage,
    list_by_item_age,
    list_by_item_state,
    list_by_state_and_age,
    list_by_type_and_age,
    list_by_type_and_state,
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

CLOUD_PROVIDERS = ["aws", "azure", "gcp"]
ITEM_TYPES = ["operational", "digital-twin", "aggregate"]
ITEM_STATES = ["provisioned", "started", "active", "error", "stopped", "suspended"]
BASE_URL = "http://localhost:3000"

logger = logging.getLogger(__name__)
console = Console(record=True)


@click.command()
@click.option("--email", "-e", help="Username")
@click.option("--password", "-p", help="Password")
@click.option("--json", is_flag=True, help="Default to output in JSON format")
def config(email: str, password: str, json: bool) -> None:
    """Stores access token and global settings of the user.

    Args:
        url (str): Mesh API url TODO
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
@click.option(
    "--state",
    help="list items by state e.g. xbot node ls --state active",
    type=click.Choice(ITEM_STATES),
)
@click.option(
    "--type",
    help="list by item type e.g. xbot node ls --type operational",
    type=click.Choice(ITEM_TYPES),
)
@click.option(
    "--interface",
    help=(
        "provide the node_id to view interfaces on that node: "
        "`xbot node ls --interface <node_id>`"
    ),
)
@click.option(
    "--age",
    help="list items provisioned within a certain timeframe e.g. xbot node ls --age 55",
    type=int,
)
@click.option("--json", "-j", is_flag=True, help="print more output.")
def ls(
    all: str, state: str, age: int, interface: str, type: str, json: bool = False
) -> None:
    """List items in the mesh.

    Args:
        state (str): list items by state. Defaults to all states available.
        type (str): list items by type.
        interface (str): provide the node_id to view all interfaces on that node.
            Example: `xbot node ls --interface <node_id>`
        age (int): number of days search criteria should apply to.
        json (bool): whether to print the data in JSON format. Defaults to False.
    """
    target_item = sys.argv[1] if len(sys.argv) > 1 else "node"
    if len(sys.argv) > 4:
        parameter = sys.argv[4]
    else:
        parameter = None
    url = f"{BASE_URL}/{target_item}s"
    response = request_data(url)
    if target_item == "node" or target_item == "port":
        if response is not None:
            if all:
                print_search(target_item, response, json)
            elif state and age:
                response = list_by_state_and_age(age, state, target_item, json)
                print_search(target_item, response, json)
            elif type and age:
                response = list_by_type_and_age(age, type, target_item, json)
                print_search(target_item, response, json)
            elif type and state:
                response = list_by_type_and_state(type, state, target_item, json)
                print_search(target_item, response, json)
            elif state:
                response = list_by_item_state(state, target_item, json)
                print_search(target_item, response, json)
            elif type:
                response = search_by_type(target_item, parameter)
                print_search(target_item, response, json)
            elif interface:
                response = search_by_interface("interface", parameter)
                print_search("interface", response, json)
            elif age:
                response = list_by_item_age(age, target_item, json)
                print_search(target_item, response, json)
            else:
                console.print(
                    (
                        "Hmm, I'm not sure what you want me to do. "
                        f"Try [bold green]`xbot {target_item} ls --all`[/bold green] "
                        f"to view all {target_item}s, or "
                        "[bold green]`xbot {target_item} ls --help`[/bold green] "
                        "for more options."
                    )
                )


@click.command()
@click.option(
    "--include-schema",
    is_flag=True,
    help="Include schema definition functions in output.",
)
@click.option("--json", "-j", is_flag=True, help="print more output.")
def ls_interfaces(
    include_schema: bool = False,
    json: bool = False,
) -> None:
    """List items in the mesh.

    Args:
        json (bool): whether to print the data in JSON format. Defaults to False.
    """
    url = f"{BASE_URL}/interfaces"
    response = request_data(url)
    if response is not None:
        print_interface_results(response, include_schema, json)


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
    """
    List the total number of items present in the mesh. Example:
        `xbot node list --total`
        will list the total number of items in the mesh.
    """
    target_item = sys.argv[1]
    url = f"{BASE_URL}/{target_item}s"
    response = request_data(url)
    response = response.json()
    console.print(
        f"There are [bold red]{len(response)} [/bold red]{target_item}s in your mesh."
        + "\n"
    )


@click.command()
@click.argument("id", type=str)
@click.option("--tree", is_flag=True, help="print as ancestor tree")
@click.option("--json", "-j", is_flag=True, help="print output in JSON format.")
def descendants(id: str, tree: bool = False, json: bool = False) -> None:
    """View the descendants of a node.

    Args:
        id (str): Node ID of the node you wish to view ancestors of.

        Example: `xbot node descendants {node_id}`.
        Hint: If you're uncertain of the ID of a node, use the
        `xbot node ls` command to find it.
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

        Example: `xbot node ancestors {node_id}`.
        Hint: If you're uncertain of the ID of a node, use the
        `xbot node ls` command to find it.
    """

    requested_data = fetch_lineage(id)
    print_lineage(requested_data, id, "ancestor", tree, json=json)

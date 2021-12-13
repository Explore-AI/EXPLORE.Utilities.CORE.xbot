import requests
from requests.structures import CaseInsensitiveDict
import json

from xbot_modules.node_functions import *
from xbot_modules.util_functions import *

base_port_api_url = "http://localhost:3000/ports"

def list_all_ports() -> None:
    """Retrieve and list all ports in the mesh
    """
    access_token = get_access_token()
    request_url = f"{base_port_api_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    port_data = json.loads(r.text)
    if len(port_data) > 0:
        print("The following nodes have been provisioned in your mesh: \n")
        for port in port_data:
            port_number = port["port_number"]
            port_name = port["name"]
            port_state = port["port_state"]
            print(f"{port_number}: {port_name} - {port_state.upper()} \n")
    else:
        print("There are currently no active ports in your mesh.")

def list_total_ports() -> None:
    """List the total number of nodes present in the mesh.
    """
    access_token = get_access_token()
    request_url = f"{base_port_api_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    port_data = json.loads(r.text)
    if len(port_data) > 0:
        total_ports = len(port_data)
        print(f"{total_ports} ports have been provisioned in your mesh.")
    else:
        print("There are currently no active nodes in your mesh.")


def list_by_port_state(state: str) -> None:
    """This function lists all ports in a given state.

    Args:
        state (str): provide the state of the ports you wish to view. Options are open or closed.
    """
    access_token = get_access_token()
    request_url = f"http://localhost:8085/rest/ports?port_state=eq.{state}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    port_data = json.loads(r.text)
    if len(port_data) > 0:
        print(f"The following ports are {state.upper()} in your mesh: \n")
        for port in port_data:
            port_number = port["port_number"]
            port_name = port["name"]
            print(f"{port_number}: {port_name} \n")
    else:
        print(f"There are currently no {state} nodes in your mesh.")


def search_by_port_number(port_number: int) -> None:
    """This function searches for a port by port number.

    Args:
        port_number (int): provide the port number of the port you wish to view.
    """
    access_token = get_access_token()
    request_url = f"http://localhost:8085/rest/ports?port_number=eq.{port_number}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    port_data = json.loads(r.text)
    if len(port_data) > 0:
        print(json.dumps(port_data, indent=4, sort_keys=True))
    else:
        print(f"Port {port_number} does not exist in your mesh.")


def add_new_port() -> None:
    """This function adds a new port to the mesh. The user is prompted to enter the node ID, port number, and port state.
    """
    access_token = get_access_token()
    node_id = input("\nEnter the node ID of the node you want to add the port to: ")
    port_number = input("\nEnter the port number of the port you want to add: ")
    port_name = input("\nEnter the name of the port: ")
    port_description = input("\nEnter a description for the port: ")
    request_url = f"http://localhost:8085/rest/ports"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.pgrst.object+json"
    headers["Authorization"] = f"Bearer {access_token}"
    headers["Prefer"] = "return=representation"
    data = {
        "node_id": node_id,
        "name": port_name,
        "port_number": port_number,
        "description": port_description,
        "port_state": "open",
    }
    response = requests.post(request_url, headers=headers, data=data)
    if response.status_code == 201:
        print("Port added successfully!\n")
        search_by_port_number(port_number)
    else:
        print(
            f"There was an error adding your port: {response.error}.\nPlease try again.\n"
        )

def delete_port(port_number: int, node_id:str) -> None:
    """Delete a port from a specific node in the mesh.

    Args:
        port_number (int): The port number of the port you wish to delete.
        
        node_id (str): The node ID of the node you wish to delete the port from.
    """
    access_token = get_access_token()
    request_url = f"{base_port_api_url}?node_id=eq.{node_id}&port_number=eq.{port_number}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    node_name = get_node_name(node_id)
    confirm_deletion = input(f"Are you sure you want to delete port {port_number} on the {node_name.upper()} node? (y/n): ")
    if confirm_deletion.lower() == "y":
        response = requests.delete(request_url, headers=headers)
        if response.status_code == 204:
            print(f"\nPort {port_number} on node{node_id} deleted successfully!\n")
        else:
            print(f"There was an error deleting your port. Status code: {response.status_code}. Error message:{response.json()['message']}")
    else:
        print("Port deletion cancelled.")
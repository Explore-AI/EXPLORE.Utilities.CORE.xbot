import requests
from requests.structures import CaseInsensitiveDict
import json
import datetime
import pytz

from xbot_modules.node_functions import *
from xbot_modules.util_functions import *

base_node_api_url = "http://localhost:3000/nodes"

def list_all_nodes() -> None:
    """Retrieve and list all nodes in the mesh
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print("The following nodes have been provisioned in your mesh: \n")
        for node in node_data:
            node_name = node["name"]
            node_id = node["id"]
            print(f"{node_name}: {node_id} \n")
    else:
        print("There are currently no active nodes in your mesh.")

def list_total_nodes() -> None:
    """List the total number of nodes present in the mesh.
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        total_nodes = len(node_data)
        print(f"{total_nodes} nodes have been provisioned in your mesh.")
    else:
        print("There are currently no active nodes in your mesh.")

def search_by_name(node_name: str) -> None:
    """Search for a node by name.

    Args:
        node_name (str): The name of the node to search for.
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?name=phfts.{node_name}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    print(json.dumps(node_data, indent=4, sort_keys=True))
    
def search_by_id(node_id: str) -> None:
    """Search for a node by ID.

    Args:
        node_id (str): The ID of the node to search for.
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?id=eq.{node_id}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    print(json.dumps(node_data, indent=4, sort_keys=True))


def list_by_state(state: str) -> None:
    """List nodes based state.

    Args:
        state (str): The state of the node to search for. Options include "provisioned", "started", "active", "error", "stopped", and "suspended". 
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?node_state=eq.{state}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print(f"The following {state.upper()} nodes have been provisioned in your mesh: \n")
        for node in node_data:
            node_name = node["name"]
            node_id = node["id"]
            print(f"{node_name}: {node_id} \n")
    else:
        print(f"There are currently no {state} nodes in your mesh.")


def list_by_cloud_provider(cloud_provider: str) -> None:
    """List nodes based on the cloud provider they're running on.

    Args:
        cloud_provider (str): The cloud provider of the node to search for. Options include "aws", "azure", and "gcp".
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?node_cloud_provider=eq.{cloud_provider}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print(f"The following {cloud_provider.upper()} nodes have been provisioned in your mesh: \n")
        for node in node_data:
            node_name = node["name"]
            node_id = node["id"]
            print(f"{node_name}: {node_id} \n")
    else:
        print(
            "There are currently no active "
            + str(cloud_provider).upper()
            + " nodes in your mesh."
        )


def list_by_node_category(node_category: str) -> None:
    """List nodes based on their category.

    Args:
        node_category (str): The category of the node to search for. Options include "source", "ingest", "enrich" and "serve".
    """
    access_token = get_access_token()
    request_url = (
        f"{base_node_api_url}?node_category=eq.{node_category}"
    )
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print(
            f"The following {node_category.upper()} nodes are active in your mesh: \n"
        )
        for node in node_data:
            node_name = node["name"]
            node_id = node["id"]
            print(f"{node_name}: {node_id} \n")

    else:
        print(f"There are currently no {node_category} nodes in your mesh.")


def list_by_node_type(node_type: str) -> None:
    """List nodes based on their type.

    Args:
        node_type (str): The type of the node to search for. Options include "digital-twin", "aggregate", and "operational".
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?node_type=eq.{node_type}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print(f"The following {node_type.upper()} nodes are active in your mesh: \n")
        for node in node_data:
            node_name = node["name"]
            node_id = node["id"]
            print(f"{node_name}: {node_id} \n")
    else:
        print(f"There are currently no {node_type} nodes in your mesh.")


def list_by_date(days_ago: int) -> None:
    """List nodes based on the date they were created.

    Args:
        days_ago (int): Provide the number of days to search for, e.g. "1" for the last day, "7" for the last week, etc.
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print(f"The following nodes were provisioned in the last {days_ago} days: \n")
    for node in node_data:
        node_time = node["date_created"]
        node_created_at = datetime.datetime.strptime(
            node_time, "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        current = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        tz = pytz.timezone("Africa/Johannesburg")
        current_time = current.astimezone(tz)
        is_within_range = current_time <= node_created_at + datetime.timedelta(
            days=days_ago
        )
        days_since_creation = (current_time - node_created_at).days
        if is_within_range:
            print(
                f"{node['name']}: {days_since_creation} days old"
            )
        else:
            print(f"There are currently no provisioned nodes in your mesh.")


def add_new_node() -> None:
    """
    This function will add a new node to the mesh.

    The user will be prompted to enter the node name, domain, and node description, and cloud provider.
    The node ID is calculated by combining the node name and domain and getting the SHA256 hash of that string.
    """
    access_token = get_access_token()
    
    node_name = input("\nEnter the name of the node: ")
    domain = input("\nEnter the domain of the node: ")
    node_description = input("\nEnter a description for the node: ")
    node_cloud_provider = input("\nEnter the cloud provider for the node: ")
    # node_id_params = f"{node_name}.{domain}"
    # node_id = hashlib.sha256(node_id_params.encode())
    # node_id = node_id.hexdigest()
    
    request_url = f"http://localhost:8085/rest/nodes"
    headers = CaseInsensitiveDict()
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.pgrst.object+json"
    headers["Authorization"] = f"Bearer {access_token}"
    headers["Prefer"] = "return=representation"
    data = {
        "name": node_name,
        "domain": domain,
        "description": node_description,
        "node_cloud_provider": node_cloud_provider,
    }
    response = requests.post(request_url, headers=headers, data=data)
    if response.status_code == 201:
        print("\nNode added successfully!\n")
        search_by_name(node_name)
    else:
        print(f"There was an error creating your node. Status code: {response.status_code}. Error message:{response.json()['message']}")
        
def delete_node(node_id:str) -> None:
    """Delete a node from the mesh.

    Args:
        node_id (str): The ID of the node to delete.
    """
    if node_id == "":
        print("\nPlease include the ID of the node you want to delete.\n")
    else:
        access_token = get_access_token()
        request_url = f"{base_node_api_url}?id=eq.{node_id}"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {access_token}"
        node_name = get_node_name(node_id)
        confirm_deletion = input(f"Are you sure you want to delete the {node_name.upper()} (ID: {node_id})? (y/n): ")
        if confirm_deletion.lower() == "y":
            response = requests.delete(request_url, headers=headers)
            if response.status_code == 204:
                print(f"\nNode {node_id} deleted successfully!\n")
            else:
                print(f"There was an error deleting your node. Status code: {response.status_code}. Error message:{response.json()['message']}")
        

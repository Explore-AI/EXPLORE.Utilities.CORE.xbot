import requests
from requests.structures import CaseInsensitiveDict
import json
import datetime
import pytz
import hashlib

from xbot_modules.node_functions import *
from xbot_modules.auth_functions import *

base_node_api_url = "http://localhost:8085/rest/nodes"

def list_all_nodes():
    access_token = get_access_token()
    request_url = f"{base_node_api_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print("The following nodes have been provisioned in your mesh: \n")
        print(json.dumps(node_data, indent=4, sort_keys=True))
    else:
        print("There are currently no active nodes in your mesh.")

def list_total_nodes() -> None:
    access_token = get_access_token()
    request_url = f"{base_node_api_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        total_nodes = len(node_data)
        print(f"{total_nodes} nodes have been provisioned in your mesh.\n")
    else:
        print("There are currently no active nodes in your mesh.")

def search_by_name(node_name: str) -> None:
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?name=eq.{node_name}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    print(json.dumps(node_data, indent=4, sort_keys=True))
    
def search_by_id(node_id: str) -> None:
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?id=eq.{node_id}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    print(json.dumps(node_data, indent=4, sort_keys=True))

def get_node_name(node_id: str) -> str:
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?id=eq.{node_id}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    return node_data[0]["name"]

def list_by_state(state: str) -> None:
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?node_state=eq.{state}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print(json.dumps(node_data, indent=4, sort_keys=True))
    else:
        print(f"There are currently no {state} nodes in your mesh.")


def list_by_cloud_provider(cloud_provider):
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?node_cloud_provider=eq.{cloud_provider}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print(
            "The following "
            + str(cloud_provider).upper()
            + " nodes are active in your mesh: \n"
        )
        print(json.dumps(node_data, indent=4, sort_keys=True))

    else:
        print(
            "There are currently no active "
            + str(cloud_provider).upper()
            + " nodes in your mesh."
        )


def list_by_node_category(node_category):
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
        print(json.dumps(node_data, indent=4, sort_keys=True))

    else:
        print(f"There are currently no {node_category} nodes in your mesh.")


def list_by_node_type(node_type: str) -> None:
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?node_type=eq.{node_type}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    if len(node_data) > 0:
        print(f"The following {node_type} nodes are active in your mesh: \n")
        print(json.dumps(node_data, indent=4, sort_keys=True))
    else:
        print(f"There are currently no {node_type} nodes in your mesh.")


def list_by_date(days_ago):
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
                f"{node['name']} --------------> {days_since_creation} days old"
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
    if node_id == "":
        print("\nPlease include the ID of the node you want to delete.\n")
    else:
        access_token = get_access_token()
        request_url = f"{base_node_api_url}?id=eq.{node_id}"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.delete(request_url, headers=headers)
        if response.status_code == 204:
            print(f"\nNode {node_id} deleted successfully!\n")
        else:
            print(f"There was an error deleting your node. Status code: {response.status_code}. Error message:{response.json()['message']}")
        

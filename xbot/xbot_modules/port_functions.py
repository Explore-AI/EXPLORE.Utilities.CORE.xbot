import requests
from requests.structures import CaseInsensitiveDict
import json
from xbot_modules.node_functions import *


def list_by_port_state(state: str) -> None:
    access_token = get_access_token()
    request_url = f"http://localhost:8085/rest/ports?port_state=eq.{state}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    port_data = json.loads(r.text)
    if len(port_data) > 0:
        print(f"The following ports are {state.upper()} in your mesh: \n")
        print(json.dumps(port_data, indent=4, sort_keys=True))
    else:
        print(f"There are currently no {state} nodes in your mesh.")


def search_by_port_number(port_number: int) -> None:
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
        search_by_port_number(port_number, access_token)
    else:
        print(
            f"There was an error adding your port: {response.error}.\nPlease try again.\n"
        )

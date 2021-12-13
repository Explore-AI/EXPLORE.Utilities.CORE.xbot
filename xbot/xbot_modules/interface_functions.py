import requests
from requests.structures import CaseInsensitiveDict
import json

from xbot_modules.util_functions import *

base_url = "http://localhost:3000/interfaces"

def view_node_interfaces(node_id: str) -> None:
    """View interfaces available on a specific node.

    Args:
        node_id (str): the node ID for the node you want to view interfaces for.
    """
    access_token = get_access_token()
    request_url = f"{base_url}?node_id=eq.{node_id}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    interface_data = json.loads(r.text)
    if len(interface_data) > 0:
        print(json.dumps(interface_data, indent=4, sort_keys=True))
    else:
        print("There are currently no interfaces available in your mesh.")
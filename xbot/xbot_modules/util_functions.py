import requests
from requests.structures import CaseInsensitiveDict
import json
import os
from dotenv import load_dotenv
load_dotenv()

base_node_api_url = "http://localhost:3000/nodes"

def get_access_token() -> str:
    """Generates an access token required to make requests to the API.

    Returns:
        str: JWT access token that is used in the headers of all requests.
    """
    user_email = os.getenv("user_email")
    user_password = os.getenv("user_password")
    url = "http://localhost:3000/rpc/login"
    response = requests.post(url, json={"email": user_email, "password": user_password})
    if response.status_code == 200:
        token = response.json()["token"]
        print(token)
        return token
    else:
        print("The details you entered are incorrect, please try again")
        get_access_token()

def get_node_name(node_id: str) -> str:
    """Get the name of a specific node.

    Args:
        node_id (str): the ID of the node you want to retrieve the name of.

    Returns:
        str: the name of the node with the given ID.
    """
    access_token = get_access_token()
    request_url = f"{base_node_api_url}?id=eq.{node_id}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    r = requests.get(request_url, headers=headers)
    node_data = json.loads(r.text)
    return node_data[0]["name"]
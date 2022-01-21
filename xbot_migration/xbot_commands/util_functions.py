import json
import os

import click
import requests

from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

load_dotenv()

base_node_api_url = "http://localhost:3000/nodes"


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


def request_data(base_url):
    access_token = get_access_token()
    request_url = f"{base_url}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    response = requests.get(request_url, headers=headers)
    target_data = json.loads(response.text)
    formatted_data = json.dumps(target_data, indent=4, sort_keys=True)
    return formatted_data

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token() -> str:
    user_email = os.getenv("user_email")
    user_password = os.getenv("user_password")
    url = "http://localhost:8085/rest/rpc/login"
    response = requests.post(url, json={"email": user_email, "password": user_password})
    if response.status_code == 200:
        token = response.json()["token"]
        return token
    else:
        print("The details you entered are incorrect, please try again")
        get_access_token()
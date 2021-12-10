import argparse
from xbot_modules.port_functions import *
from xbot_modules.node_functions import *

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIiA6ICJ3ZWJ1c2VyIiwgInVzZXJfaWQiIDogMSwgImV4cCIgOiAxNjM5MTM4MTA4fQ.uCI3l56PHuPVxgbqRfPjseet8oUk3YPd6THSWXP7bko"


def get_access_token() -> str:
    user_email = input("Enter your email: ")
    user_password = input("Enter your password: ")
    url = "http://localhost:8085/rest/rpc/login"
    response = requests.post(url, json={"email": user_email, "password": user_password})
    if response.status_code == 200:
        token = response.json()["token"]
        print("Successfully authenticated \n")
        print(token)
        return token
    else:
        print("The details you entered are incorrect, please try again")
        get_access_token()


def set_access_token(token) -> None:
    global access_token
    access_token = token


# try:
#     access_token
# except NameError:
#     token = get_access_token()
#     set_access_token(token)


parser = argparse.ArgumentParser(
    description="A command line tool to visualise the current state your data mesh."
)

parser.add_argument(
    "-l", "-login", help="provide credentials to login to the mesh", action="store_true"
)
parser.add_argument(
    "-a", "-all", help="list all nodes in the mesh", action="store_true"
)
parser.add_argument(
    "-s",
    "-state",
    choices=["provisioned", "started", "active", "error", "stopped", "suspended"],
    help="list nodes in your mesh based on their state",
)
parser.add_argument(
    "-ps",
    "-port_state",
    choices=["open", "closed"],
    help="list nodes in your mesh based on their port state",
)
parser.add_argument(
    "-pn",
    "-port_number",
    type=int,
    help="search for nodes in your mesh based on their port number",
)
parser.add_argument(
    "-c",
    "-cloud",
    choices=["aws", "azure", "gcp"],
    help="list active nodes by cloud provider, for example -c aws",
)
parser.add_argument(
    "-cat",
    "-category",
    choices=["source", "ingest", "enrich", "serve"],
    help="list active nodes by cloud provider, for example -c aws",
)
parser.add_argument(
    "-t",
    "-type",
    choices=["digital-twin", "aggregate", "operational"],
    help="list active nodes by node type, for example -t operational",
)
parser.add_argument(
    "-d",
    "-date",
    type=int,
    help="list nodes created in the last X days, for example -date 30 to view nodes created in the last 30 days",
)

parser.add_argument(
    "-ap", "-add_port", help="add a port to a node.", action="store_true"
)
parser.add_argument(
    "-an", "-add_node", help="add a new node to the mesh", action="store_true"
)
parser.add_argument(
    "-n",
    "-name",
    help="search for a node by name.",
)
parser.add_argument(
    "-id",
    help="search for a node by name.",
)

args = parser.parse_args()

if args.l:
    get_access_token()
if args.a:
    list_all_nodes(access_token)
if args.s:
    state = str(args.s)
    list_by_state(state, access_token)
if args.c:
    cloud_provider = str(args.c)
    list_by_cloud_provider(cloud_provider, access_token)
if args.cat:
    node_category = str(args.cat)
    list_by_node_category(node_category, access_token)
if args.t:
    node_type = str(args.t)
    list_by_node_type(node_type, access_token)
if args.d:
    days_ago = int(args.d)
    list_by_date(days_ago, access_token)
if args.ps:
    port_state = str(args.ps)
    list_by_port_state(port_state, access_token)
if args.pn:
    port_number = int(args.pn)
    search_by_port_number(port_number, access_token)
if args.ap:
    add_new_port(access_token)
if args.an:
    add_new_node(access_token)
if args.n:
    node_name = str(args.n)
    search_by_name(access_token, node_name)
if args.id:
    node_id = str(args.id)
    search_by_id(access_token, node_id)

if __name__ == "__main__":
    parser.parse_args()

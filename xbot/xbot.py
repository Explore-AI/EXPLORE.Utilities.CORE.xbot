import argparse
from xbot_modules.util_functions import * 
from xbot_modules.port_functions import *
from xbot_modules.node_functions import *
from xbot_modules.interface_functions import *

user_email = "alice@email.com"
user_password = "pass"

parser = argparse.ArgumentParser(
    description="A command line tool to visualise the current state your data mesh."
)

parser.add_argument(
    "-l", "-login", help="provide credentials to login to the mesh", action="store_true"
)
parser.add_argument(
    "-all_nodes", help="list all nodes in the mesh", action="store_true"
)
parser.add_argument(
    "-all_ports", help="list all ports in the mesh", action="store_true"
)
parser.add_argument(
    "-total_nodes", help="list total number of nodes in the mesh", action="store_true"
)
parser.add_argument(
    "-total_ports", help="list total number of nodes in the mesh", action="store_true"
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
    "-delete_node", help="delete a node from your mesh"
)
parser.add_argument(
    "-delete_port", nargs=2, help="delete a port from a node"
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
parser.add_argument(
    "-i",
    "-interface",
    help="search for available interfaces on a specific node. Requires you to provide a node id.",
)
parser.add_argument(
    "-launch_node",
    help="launch a node",
    action="store_true",
)
parser.add_argument(
    "-view_ancestors",
    help="view the ancestors of a node",
)
parser.add_argument(
    "-view_descendants",
    help="view the ancestors of a node",
)
parser.add_argument(
    "-get_schema",
    help="view the ancestors of a node",
)

args = parser.parse_args()

if args.l:
    get_access_token()
if args.all_nodes:
    list_all_nodes()
if args.all_ports:
    list_all_ports()
if args.s:
    state = str(args.s)
    list_by_state(state)
if args.c:
    cloud_provider = str(args.c)
    list_by_cloud_provider(cloud_provider)
if args.cat:
    node_category = str(args.cat)
    list_by_node_category(node_category)
if args.t:
    node_type = str(args.t)
    list_by_node_type(node_type)
if args.d:
    days_ago = int(args.d)
    list_by_date(days_ago)
if args.ps:
    port_state = str(args.ps)
    list_by_port_state(port_state)
if args.pn:
    port_number = int(args.pn)
    search_by_port_number(port_number)
if args.ap:
    add_new_port()
if args.an:
    add_new_node()
if args.n:
    node_name = str(args.n)
    search_by_name(node_name)
if args.id:
    node_id = str(args.id)
    search_by_id(node_id)
if args.i:
    node_id = str(args.i)
    view_node_interfaces(node_id)
if args.total_nodes:
    list_total_nodes()
if args.total_ports:
    list_total_ports()
if args.delete_node:
    node_id = str(args.delete)
    delete_node(node_id)
if args.delete_port:
    port_number = str(args.delete_port[0])
    node_id = str(args.delete_port[1])
    delete_port(port_number, node_id)
if args.launch_node:
    launch_node()
if args.view_ancestors:
    node_id = str(args.view_ancestors)
    view_ancestors(node_id)
if args.view_descendants:
    node_id = str(args.view_descendants)
    view_descendants(node_id)
if args.get_schema:
    node_id = str(args.get_schema)
    get_schema(node_id)

if __name__ == "__main__":
    parser.parse_args()

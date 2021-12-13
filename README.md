# xbot CLI
The Command Line Interface for creating and interacting with a running Mesh instance within the EXPLORE CORE Platform.

## Building this package locally
`python setup.py sdist`

## Installing this package from GitHub
`pip install -e "git+https://github.com/Explore-AI/EXPLORE.Utilities.CORE.xbot#egg=xbot"`

Install the required dependencies: `pip install -r requirements.txt`
# How to use this package

The command above will create a `src` folder and install the `xbot-cli` package in it with the name. Navigate through these folders to the `xbot` folder (`cd src/xbot-cli/xbot`) and run `python xbot.py -h` to see a list of commands.

The following commands are available on the command line interface, with their usage explained below. You can view all possible commands and the arguments they accept by running `python xbot.py -h`. 
## Querying the mesh

### Querying nodes:

- `python xbot.py -h`: displays a help message.
- `python xbot.py -l`: prompts the user to provide an email address and password to log in to the CLI and access the API.
- `python xbot.py -a` or `python xbot.py -all`: displays all nodes, their ID's, and their state (e.g. running), currently in your mesh.
- `python xbot.py -s` or `python xbot.py -state`: allows you to query nodes based on their state. Requires you to pass one of the possible states as an argument. States include "provisioned", "started", "active", "error", "stopped", "suspended". Example: `python xbot.py -s active`
- `python xbot.py -c` or `python xbot.py -cloud`: allows you to query nodes based on the cloud provider they're running on. Example: `python xbot.py -c azure`
- `python xbot.py -cat` or `python xbot.py -category`: allows you to query nodes based on their category, i.e. "source", "ingest", "enrich", or "serve". Example: `python xbot.py -cat enrich`
- `python xbot.py -cat` or `python xbot.py -category`: allows you to query nodes based on their type, i.e. "digital-twin", "aggregate", or "operational". Example: `python xbot.py -t operational`
- `python xbot.py -d` or `python xbot.py -date`: allows you to query nodes based on when they were created. Example: `python xbot.py -d 30` will display all nodes created in the last 30 days.
- `python xbot.py -n` or `python xbot.py -name`: allows you to search for a node by name. Example: `python xbot.py -n `
- `python xbot.py -id`: allows you to search for a node by ID. Example: `python xbot.py -id  27b355d7c2c6186c4a2b7d1f1381b6acfdb1f6a44bfc6651d8bb733c746433e5`

### Adding and deleting nodes:
- `python xbot.py -an` or `python xbot.py -add_node`: allows you to add a new node to the mesh. Running the command will lead to a series of prompts to collect information about the node, which will then be used to create the node. No additional arguments are required.  
- `python xbot.py -delete_node`: allows you to delete a node by providing the node ID. Example: `python xbot.py -delete_node 43584d4d8d6ee7f879f6ca9e38e164d21b19576ddfd0231dfe9354caddc9b471`
---
### Querying ports: 

- `python xbot.py -ps` or `python xbot.py -port_state`: allows you to query ports based on their state i.e. open or closed. Example: `python xbot.py -ps open`
- `python xbot.py -pn` or `python xbot.py -port_number`: allows you to search for port information based on port number. Example: `python xbot.py -pn 300`

### Adding and deleting ports:
- `python xbot.py -ap` or `python xbot.py -add_port`: allows you to add a new port to the mesh. Running the command will display the nodes that currently exist in the mesh and will ask you to select and input the ID of the node that you wish to add the port to, before asking for additional information. 
- `python xbot.py -delete_port`: allows you to delete a port by providing the port number and the node ID of the node where the port can be found. Example: `python xbot.py -delete_port 3000 43584d4d8d6ee7f879f6ca9e38e164d21b19576ddfd0231dfe9354caddc9b471` will delete port 3000 on the node with the given ID. It's necessary to supply both the port number and the node ID because a port with the same number can exist on multiple nodes. 
---
### Querying interfaces:
- `python xbot.py -i` or `python xbot.py -interface`: allows you to retrieve the interface for a specific node by proving a node ID. Example: `python xbot.py -interface 43584d4d8d6ee7f879f6ca9e38e164d21b19576ddfd0231dfe9354caddc9b471`

# Request for feedback

This CLI is still in development and any feedback and comments would be appreciated. When testing, please think about how to make the user experience simpler and more intuitive. If there are parts of it that feel like they're surfacing too much information, or too little information, please let us know. 

You can note all feedback and comments on [this Notion page](https://www.notion.so/exploreutils/xbot-Feedback-707fffa4a706419bb165606940619b0c), or email core-platform@explore-utilities.com.

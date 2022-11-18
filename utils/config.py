import argparse
import json
import os

# Project Path Constents
PROJECT_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/..")
SRC_PATH = os.path.abspath(PROJECT_ROOT_PATH + "/src")
UTILS_PATH = os.path.abspath(PROJECT_ROOT_PATH + "/utils")
CONFIG_FILE_PATH = os.path.abspath(UTILS_PATH + "/config.json")

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-n", "--new-board", help = "Add a new board to the system.")
parser.add_argument("-s", "--system", help = "Configure full system from scratch.")
 
# Read arguments from command line
args = parser.parse_args()

print(args)
 
# Read Current Config File.
config = {}
try:
    file = open(CONFIG_FILE_PATH, 'r')
    config = json.loads(file.read())
    file.close()
except: 
    print("No existing config file found.")

SYSTEM_KEY = "system"
NODES_KEY = "nodes"

update_system_config = False
if config.get(SYSTEM_KEY) == None:
    print("No existing System Configuration")
    update_system_config = True
elif config.get(SYSTEM_KEY) != None:
    print("Current System Config:")
    print(json.dumps(config.get(SYSTEM_KEY), indent = 4))
    if input("Update System Config? (Y/n) ").upper() == "Y":
        update_system_config = True

if update_system_config:
    system_config = {}
    system_config["ssid"] = input("Network SSID: ")
    system_config["password"] = input("Network Password ")
    config[SYSTEM_KEY] = system_config


update_nodes = False
if config.get(NODES_KEY) == None:
    print("No existing Nodes")
    config[NODES_KEY] = {}
    update_nodes = True
elif config.get(NODES_KEY) != None:
    print("Current Nodes Config:")
    print(json.dumps(config.get(NODES_KEY), indent = 4))
    if input("Create or Update Node Config? (Y/n) ").upper() == "Y":
        update_nodes = True

if update_nodes:
    print("Use existing node name to update or new node name to create.")
    node_config = {}
    node_name = input("Node Name: ")
    node_config["ip_address"] = input("IP Address: ")
    node_config["correction_value"] = input("Sensor Correction Value in Celsius: ")
    config[NODES_KEY][node_name] = node_config

print("Final Config: ")
print(json.dumps(config, indent = 4))

if input("Write config? (Y/n): ").upper() == "Y":
    file = open(CONFIG_FILE_PATH, 'w')
    file.write(json.dumps(config, indent = 4))
    file.close()

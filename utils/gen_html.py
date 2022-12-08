import json
import os

# Project Path Constents
PROJECT_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/..")
SRC_PATH = os.path.abspath(PROJECT_ROOT_PATH + "/src")
UTILS_PATH = os.path.abspath(PROJECT_ROOT_PATH + "/utils")
CONFIG_FILE_PATH = os.path.abspath(UTILS_PATH + "/config.json")
 
# Read Current Config File.
config = {}
try:
    with open(CONFIG_FILE_PATH, "r") as config_input_file:
        config = json.loads(config_input_file.read())
except: 
    print("No existing config file found.")

NODES_KEY = "nodes"

header = "<!doctype html>\n<html>\n<head>\n\t<title>Dashboard</title>\n<link rel=\"stylesheet\" href=\"/styles/dashboard.css\">\n</head>\n<body>\n"
body = ""
if config.get(NODES_KEY) != None:
    for node in config.get(NODES_KEY).keys():
        ip_address = config.get(NODES_KEY)[node]['ip_address']
        iframeTag = f"\t<iframe class=\"frameContainer\" src='http://{ip_address}/chart'></iframe>\n"
        body = body + iframeTag

footer = "</html>"


with open(os.path.abspath(SRC_PATH + "/web/html/dashboard.html"), "w") as dashboard_output_file: 
    dashboard_output_file.write(header)
    dashboard_output_file.write(body)
    dashboard_output_file.write(footer)
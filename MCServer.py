#!/usr/bin/env python3
import json
import os
import requests
import sys
import urllib.parse

VERBOSE = False

script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

config = {
  "server_software": "fabric",
  "server_version": "1.16.5",
  "serverjar_name": "Launcher.jar",

  "server_min_ram": 512,
  "server_max_ram": 2_048,
  "hide_server_gui": True,

  "modrinth_user_agent": "othecat35/mcserver",
  "modrinth_api_url": "https://api.modrinth.com/v2/"
}

colors = {
  "gray": "\033[90m",
  "green": "\033[32m",
  "red": "\033[31m",
  "reset": "\033[0m",
  "yellow": "\033[33m"
}

def color(color_name):
  if sys.stdout.isatty:
    return f"{colors[color_name]}"

def logger(log_level, message):
  log_level = log_level.lower()
  if log_level == "debug" and not VERBOSE:
    return

  print(f"[{log_level.upper()}]: {message}")

def init():
  logger("info", f"Initializing setup...")
  try:
    os.mkdir(script_name)
  except Exception as error:
    logger("error", f"Cannot create directory \"{script_name}\": {error}")

def load_config(section):
  config_file_path = os.path.join(script_name, "config.json")

  try:
    with open(config_file_path) as config_file:
      config_json = json.load(config_file)[section]
      return config_json
  except:
    pass

def search_mod(query):
  search_filters = f"[[\"project_type:mod\"],\
[\"server_side:optional\"],\
[\"categories:{config['server_software']}\"],\
[\"versions:{config['server_version']}\"]]"

  url = urllib.parse.urljoin(config["modrinth_api_url"], f"search\
?limit=20\
&facets={search_filters}\
&query={query}")

  logger("debug", f"Fetching URL: {url}")
  response_json = json.loads(requests.get(url, headers={
    "User-Agent": config["modrinth_user_agent"]
  }).text)

  logger("debug", f"Got response: \n{json.dumps(response_json, indent=2)}")
  if len(response_json["hits"]) < 1:
    logger("error", "No mod found.")
    sys.exit(1)

  mods_list = response_json["hits"]

  for mod in mods_list:
    print(f"""\
{color("green")}{mod["slug"]}{color("reset")}/modrinth
  {mod["description"]}
""")

def start_server():
  server_command_args = [
    "java",
    f"-Xms{config['server_min_ram']}",
    f"-Xmx{config['server_max_ram']}",
    "-jar", config["serverjar_name"]
  ]

  if config["hide_server_gui"]:
    server_command_args.append("nogui")

  logger("info", "Starting the server...")
  os.execvp("java", server_command_args)

def main():
  script_args = sys.argv[1:] if len(sys.argv) > 1 else [""]

  command = script_args[0]
  command_args = " ".join(script_args[1:]) if len(script_args) > 1 else ""

  if not os.path.isdir(script_name):
    logger("error", f"{script_name} director does not exist!")
    init()

  match command:
    case "search":
      search_mod(command_args)
    case "start":
      start_server()
    case _:
        logger("error", f"Not a valid command {command}")
        sys.exit(1)

if __name__ == "__main__":
  main()

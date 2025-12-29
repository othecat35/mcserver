#!/usr/bin/env python3
import json
import os
import requests
import sys
import urllib.parse

VERBOSE = True

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

def logger(log_level, message):
  log_level = log_level.lower()
  if log_level == "debug" and not VERBOSE:
    return

  print(f"[{log_level.upper()}]: {message}")

def search_mod(query):
  search_filters = f"[[\"project_type:mod\"],\
[\"server_side:required\"],\
[\"categories:{config['server_software']}\"],\
[\"versions:{config['server_version']}\"]]"

  url = urllib.parse.urljoin(config["modrinth_api_url"], f"search\
?limit=1\
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

  mod = response_json["hits"][0]

  print(f"""\
Name        : {mod['title']}
Creator     : {mod['author']}
Description : {mod['description']}""")

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
  command = sys.argv[1] if len(sys.argv) > 1 else "start"
  command_args = sys.argv[2] if len(sys.argv) > 2 else ""

  match command:
    case "search":
      logger("info", "Searching mod in Modrinth...")
      search_mod(command_args)
    case "start":
      start_server()
    case _:
      logger("error", f"Unknown command: {command}")

if __name__ == "__main__":
  main()
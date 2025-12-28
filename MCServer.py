#!/usr/bin/env python3
import os
import sys

config = {
  "server_min_ram": 512,
  "server_max_ram": 2_048,

  "serverjar_name": "Launcher.jar",
  "hide_server_gui": True
}

def start_server():
  server_command_args = [
    "java",
    f"-Xms{config['server_min_ram']}",
    f"-Xmx{config['server_max_ram']}",
    "-jar", config['serverjar_name']
  ]

  if config["hide_server_gui"]:
    server_command_args.append("nogui")

  print("[INFO]: Starting the server...")
  os.execvp("java", server_command_args)

def main():
  command = sys.argv[1] if len(sys.argv) > 1 else "start"

  match command:
    case "start":
      start_server()
    case _:
      print(f"[ERROR]: Unknown command: {command}")

if __name__ == "__main__":
  main()
#!/usr/bin/env python3

import os
import sys
import json
from textwrap import dedent
from random import randint

list_tasks_argv = ["-l", "--list"]
stop_tasks_argv = ["-s", "--stop"]
restart_tasks_argv = ["-r", "--restart"]

def getUser() -> str:
    try:
        return os.environ["SUDO_USER"]
    except KeyError:
        return os.environ["USER"]

def new() -> str:
    cmd = ""
    for i in sys.argv[1:]:
        cmd += f"{i} "
    cmd = cmd.rstrip()

    id = str(randint(1, 65535))
    while os.path.exists(f"/etc/systemd/system/{id}-ack.service"):
        id = str(randint(1, 65535))

    path = os.getcwd()
    user = getUser()

    with open(f"/etc/systemd/system/{id}-ack.service", "w+") as file:
        systemd = dedent(f"""
            [Unit]
            Description={id}-ack Background service
            After=network.target

            [Service]
            User={user}
            WorkingDirectory={path}
            ExecStart={cmd}

            [Install]
            WantedBy=multi-user.target
        """)
        file.write(systemd)

    os.system("systemctl daemon-reload")
    os.system(f"systemctl start {id}-ack")

    try:
        if os.environ["ACK_CHANGED_ROOT"] == "True":
            user = os.environ["USER"]
    except KeyError:
        pass
    
    user_path = os.path.expanduser(f"~{user}") + "/.ack"
    if not os.path.exists(user_path):
        os.mkdir(user_path)

    config = {"cmd": cmd, "id": id, "user": user}
    with open(f"{user_path}/{str(id)}", "w+") as cfg:
        json.dump(config, cfg, indent=4)

    return id

def stop(id: int) -> None:
    user = getUser()
    user_path = os.path.expanduser(f"~{user}") + "/.ack"

    if not os.path.exists(user_path):
        raise FileNotFoundError("task doesn't exist")
    
    os.system(f"systemctl stop {id}-ack")
    os.remove(f"/etc/systemd/system/{id}-ack.service")
    os.system("systemctl daemon-reload")

def restart(id: int) -> None:
    user = getUser()
    user_path = os.path.expanduser(f"~{user}") + "/.ack"

    if not os.path.exists(user_path):
        raise FileNotFoundError
    
    os.system(f"systemctl restart {id}-ack")

def list() -> None:
    user = getUser()
    user_path = os.path.expanduser(f"~{user}") + "/.ack"
    num = 1

    try:
        if os.listdir(user_path):
            print("List of working daemons:")
            for tasks in os.listdir(user_path):
                with open(f"{user_path}/{tasks}", "r") as file:
                    fullpath = json.load(file)
                print(f"{num} # {tasks} \"{fullpath["cmd"]}\" as: {fullpath["user"]}")
                num += 1
        else:
            print("There is no working daemons")
    except FileNotFoundError:
        print("There is no working daemons")

def main():
    try:
        if sys.argv[1] in list_tasks_argv:
            list()
            sys.exit(0)
        elif sys.argv[1] in stop_tasks_argv:
            try:
                stop(sys.argv[2])
                print(f"Daemon with id {sys.argv[2]} was stopped")
                sys.exit(0)
            except FileNotFoundError:
                print(f"Error: task doesn't exist")
        elif sys.argv[1] in restart_tasks_argv:
            try:
                restart(sys.argv[2])
                print(f"Daemon with id {sys.argv[2]} was restarted")
                sys.exit(0)
            except FileNotFoundError:
                print(f"Error: task doesn't exist")
        elif sys.argv[1]:
            print(f"Daemon was started with ID: {new()}")
            sys.exit(0)
    except IndexError:
        print("Error: couldn't parse flags")

if __name__ == "__main__":
    if os.geteuid() == 0:
        main()
    else:
        print("Error: you must run this script as root or with 'sudo'")
        sys.exit(1)
#!/usr/bin/env python3

import sys
import datetime
from os.path import exists
from optparse import OptionParser

import paramiko
from colorama import Fore, Style, just_fix_windows_console


class Host:
    def __init__(self, text):
        self.host = None
        self.port = 22
        self.username = None
        self.password = None
        self.groups = []
        self._parse_string(text)

    def _parse_string(self, text):
        parts = text.split()

        self.host = parts[0]

        parser = OptionParser()
        parser.add_option("--port", dest="port", default=22)
        parser.add_option("--username", dest="username")
        parser.add_option("--password", dest="password", default="dummy")

        (options, args) = parser.parse_args(parts[1:])

        self.port = int(options.port)
        self.username = options.username
        self.password = options.password
        self.groups = sorted(list(set(args)))

    def _message(self, text, colour):
        styled_host = f"{Fore.BLUE + self.host + Style.RESET_ALL}"
        ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f6")
        print(f"{styled_host} : {ts} : {colour}{text}{Style.RESET_ALL}")

    def is_in_group(self, group):
        if group == None:
            return True
        else:
            return group in self.groups

    def execute(self, cmd):
        self._message(cmd, Fore.YELLOW)

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, self.port, self.username, self.password)
            stdin, stdout, stderr = ssh.exec_command(cmd)

            for line in stdout.readlines():
                l = line.strip()
                if l != "":
                    self._message(l, Fore.GREEN)
            for line in stderr.readlines():
                l = line.strip()
                if l != "":
                    self._message(l, Fore.RED)
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            self._message(str(e), Fore.RED)
        except paramiko.ssh_exception.AuthenticationException as e:
            self._message(str(e), Fore.RED)


class Machines:
    def __init__(self, filename):
        self.hosts = []

        with open(filename, "r") as f:
            for line in f:
                x = line.lower().strip()
                if not x.startswith("#") and x != "":
                    self.hosts.append(Host(x))

    def execute(self, commands, group=None):
        for host in self.hosts:
            if host.is_in_group(group):
                for cmd in commands:
                    host.execute(cmd)
                print()

    def list_hosts(self):
        list_hosts = []

        for host in self.hosts:
            list_hosts.append(host.host)

        return sorted(list_hosts)

    def list_groups(self):
        list_groups = []

        for host in self.hosts:
            for group in host.groups:
                if group not in list_groups:
                    list_groups.append(group)

        return sorted(list(set(list_groups)))


def dropdead(message):
    print(Fore.RED + message + Style.RESET_ALL)
    sys.exit(1)


def list_things(a_list):
    for x in a_list:
        print(x)


def commands_from_file(filename):
    if exists(filename):
        commands = []
        with open(filename, "r") as f:
            for line in f:
                cmd = line.strip()
                if cmd != "" and not cmd.startswith("#"):
                    commands.append(cmd)

        return commands
    else:
        dropdead(f"Command file {filename} not found")


def build_command(parts):
    if len(parts) == 1 and parts[0].startswith("@"):
        return commands_from_file(parts[0][1:])

    return [" ".join(parts)]


if __name__ == "__main__":
    just_fix_windows_console()

    parser = OptionParser()
    parser.add_option(
        "-f",
        "--file",
        dest="filename",
        default="machines.list",
        help="The file to list the avaiable machines",
        metavar="FILE",
    )
    parser.add_option(
        "-g",
        "--group",
        dest="group",
        help="The group of hosts to execute the command against",
    )
    parser.add_option(
        "-l",
        "--list",
        dest="lists",
        default=None,
        help="List the available hosts or groups",
    )

    (options, args) = parser.parse_args()

    filename = options.filename
    group = options.group
    lists = options.lists

    if args == [] and lists == None:
        dropdead("No command supplied")

    if not exists(filename):
        dropdead(f"Unable to locate: {filename}")

    m = Machines(filename)

    if lists is not None:
        if lists == "hosts":
            list_things(m.list_hosts())
        elif lists == "groups":
            list_things(m.list_groups())
        else:
            dropdead(f"Only 'hosts' and 'groups' can be listed. Not: {lists}")
        sys.exit(0)

    if group != None and group not in m.list_groups():
        dropdead(f"Unknown group: {group}")

    cmd = build_command(args)
    m.execute(cmd, group)

# TODO
# Usage report when nothing is given
# Parallel execution of commands???

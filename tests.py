#!/usr/bin/env python3

import os
import unittest

from pssh import Host, Machines


class TestHost(unittest.TestCase):
    def check_groups(self, actual, expected):
        self.assertEqual(len(actual), len(expected), "incorrect number of groups")
        self.assertEqual(actual, expected, "incorrect group membership / order")

    def test_all_the_defaults(self):
        h = Host("fred.local")
        self.assertEqual(h.host, "fred.local", "incorrect host")
        self.assertEqual(h.port, 22, "incorrect port")
        self.assertEqual(h.username, None, "incorrect username")
        self.assertEqual(h.password, "dummy", "incorrect password")
        self.check_groups(h.groups, [])

    def test_one_group(self):
        h = Host("fred.local g1")
        self.check_groups(h.groups, ["g1"])

    def test_three_groups(self):
        h = Host("fred.local g1 x999 g2")
        self.check_groups(h.groups, ["g1", "g2", "x999"])

    def test_is_in_groups(self):
        h = Host("fred.local g1 x999 g2")
        self.assertEqual(h.is_in_group("g2"), True, "group in groups")

    def test_is_not_in_groups(self):
        h = Host("fred.local g1 x999 g2")
        self.assertEqual(h.is_in_group("not-here"), False, "group not in groups")

    def test_simplify_groups(self):
        h = Host("fred.local g9 g1 g1 g2")
        self.check_groups(h.groups, ["g1", "g2", "g9"])

    def test_set_username(self):
        h = Host("fred.local --username tom")
        self.assertEqual(h.username, "tom", "username not overriden")

    def test_set_password(self):
        h = Host("fred.local --password tom")
        self.assertEqual(h.password, "tom", "password not overriden")

    def test_set_port(self):
        h = Host("fred.local --port 1234")
        self.assertEqual(h.port, 1234, "port not overridden")

    def test_set_all(self):
        h = Host(
            "fred.local --username tom group1 --port 1234 --password another group2"
        )
        self.assertEqual(h.username, "tom", "username not overriden")
        self.assertEqual(h.password, "another", "password not overriden")
        self.assertEqual(h.port, 1234, "port not overridden")
        self.check_groups(h.groups, ["group1", "group2"])


class TestMachines(unittest.TestCase):
    def build_temp(self, lines):
        with open("test_temp.txt", "w") as f:
            for line in lines:
                f.write(line)
                f.write("\n")

    def tearDown(self):
        if os.path.exists("test_temp.txt"):
            os.remove("test_temp.txt")

    def test_count_hosts(self):
        self.build_temp(["tom.local g1", "dick.local g2", "harry.local g1 g2"])
        m = Machines("test_temp.txt")
        hosts = m.list_hosts()
        self.assertEqual(len(hosts), 3, "wrong number of hosts")

    def test_count_groups(self):
        self.build_temp(["tom.local g1", "dick.local g2", "harry.local g1 g2"])
        m = Machines("test_temp.txt")
        groups = m.list_groups()
        self.assertEqual(len(groups), 2, "wrong number of groups")

    def test_ignore_comments(self):
        self.build_temp(
            ["# ignore this", "tom.local g1", "dick.local g2", "harry.local g1 g2"]
        )
        m = Machines("test_temp.txt")
        hosts = m.list_hosts()
        self.assertEqual(len(hosts), 3, "wrong number of hosts")

    def test_ignore_blank_lines(self):
        self.build_temp(
            ["", "tom.local g1", "dick.local g2", "     ", "harry.local g1 g2"]
        )
        m = Machines("test_temp.txt")
        hosts = m.list_hosts()
        self.assertEqual(len(hosts), 3, "wrong number of hosts")


unittest.main()

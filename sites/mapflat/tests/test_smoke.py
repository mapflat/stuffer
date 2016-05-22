"""Smoke test mapflat provisioning scripts. Run them, and verify that they run to completion."""

import os
import sys
import unittest


sys.path.append("{}/../../..".format(os.path.dirname(__file__)))
sys.path.append("{}/../../../tests".format(os.path.dirname(__file__)))

# noinspection PyUnresolvedReferences
from fixture import DockerTest


class SmokeTest(DockerTest):
    def test_laptop(self):
        self.stuff(["--file", "/stuffer/sites/mapflat/laptop.py"])
        # self.stuff_all_from("{}/../laptop.py".format(os.path.dirname(__file__)))
        self.assertTrue(self.container_run(["restview", "--version"]).find("2.") != -1)


if __name__ == '__main__':
    unittest.main()

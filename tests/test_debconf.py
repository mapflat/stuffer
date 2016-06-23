from pathlib import Path
import sys

import re


sys.path.append(Path(__file__).parent.parent)

import fixture


class AptSourceListTest(fixture.DockerTest):
    def test_add(self):
        self.stuff(['debconf.SetSelections("mysect", "mythings/somekey", "boolean", "true")'])
        self.assertTrue(re.search(r'mysect\s+mythings/somekey\s+boolean\s+true',
                                  self.container_run(['debconf-get-selections'])))

    def test_seen(self):
        self.stuff(['debconf.SetSelections("mysect", "mythings/something", "select", "one")'])
        self.stuff(['debconf.SetSelections("mysect", "mythings/something", "seen", "true")'])
        # debconf-show adds a * prefix for questions that have been shown
        self.assertTrue(re.search(r'\*\s+mythings/something:\s+one',
                                  self.container_run(['debconf-show', 'mysect'])))

from pathlib import Path
import sys

import re


sys.path.append(Path(__file__).parent.parent)

import fixture


class AptSourceListTest(fixture.DockerTest):
    def test_add(self):
        self.stuff(['debconf.SetSelections("mysect", "mythings/somekey", "true")'])
        self.assertTrue(re.search(r'mysect\s+mythings/somekey\s+select\s+true',
                                  self.container_run(['debconf-get-selections'])))

import sys

from pathlib import Path


sys.path.append(str(Path(__file__).parents[1]))

import fixture


class GroupAddTest(fixture.DockerTest):
    def test_set_get(self):
        self.stuff(["user.AddToGroup('mail', 'floppy')"])
        self.assertRegex(self.container_run('groups mail'), 'floppy')

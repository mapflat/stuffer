import sys

from pathlib import Path


sys.path.append(Path(__file__).parent.parent)

import fixture


class IntelliJTest(fixture.DockerTest):
    def test_install_community(self):
        self.stuff(['contrib.jetbrains.IntelliJ("2016.1.4", "145")'])
        self.assertRegex(self.container_run(['sh', '-c', 'ls /usr/local/idea-IC-145*/bin']), r'idea\.sh')

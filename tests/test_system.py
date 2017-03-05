import sys

from pathlib import Path


sys.path.append(str(Path(__file__).parents[1]))

import fixture


class SystemTest(fixture.DockerTest):
    def test_shell_command(self):
        self.stuff(["system.ShellCommand('echo new_content > /tmp/brand_new_file')"])
        self.assertRegex(self.container_run(["cat", "/tmp/brand_new_file"]), r'new_content')

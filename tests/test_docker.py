import sys

from pathlib import Path


sys.path.append(Path(__file__).parent.parent)

import fixture


class DockerTest(fixture.DockerTest):
    def test_prologue(self):
        self.stuff(['docker.Prologue()'])
        self.assertRegex(self.container_run(['cat', '/var/log/stuffer.log']), r'phusion')

    def test_epilogue(self):
        self.stuff(['apt.Install("pchar")'])
        self.stuff(['docker.Epilogue()'])
        self.assertRegex(self.container_run(['ls', '-l', '/var/lib/apt/lists']), r'total 0')

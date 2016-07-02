import re
import sys

from pathlib import Path


sys.path.append(Path(__file__).parent.parent)

import fixture


class JdkTest(fixture.DockerTest):
    def test_install_jdk_8(self):
        self.stuff(['contrib.java.Jdk(8)'])
        self.assertTrue(re.search(r'javac 1\.8\.', self.container_run(['sh', '-c', 'javac -version 2>&1'])))

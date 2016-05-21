import os
import sys


sys.path.append("{}/..".format(os.path.dirname(__file__)))

import fixture

class PipInstallTest(fixture.DockerTest):
    def test_basic_install(self):
        self.stuff(['pip.Install("restview==2.6.1")'])
        self.assert_(self.container_run(["restview", "--version"]).find("2.6.1") != -1)

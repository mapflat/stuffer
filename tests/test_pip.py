import os
import sys


sys.path.append("{}/..".format(os.path.dirname(__file__)))

import fixture

class PipInstallTest(fixture.DockerTest):
    def test_basic_install(self):
        self.stuff(['pip.Install("restview==2.6.1")'])
        self.assertRegex(self.container_run(["pip3", "list"]), r'restview \(2\.6\.1\)')

    def test_upgrade(self):
        self.stuff(['pip.Install("restview==2.6.0")'])
        self.stuff(['pip.Install("restview", upgrade=True)'])
        self.assertNotRegex(self.container_run(["pip3", "list", '--outdated']), r'restview ')

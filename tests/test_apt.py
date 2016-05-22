import os
import sys


sys.path.append("{}/..".format(os.path.dirname(__file__)))

import fixture

class AptInstallTest(fixture.DockerTest):
    def test_basic(self):
        self.stuff(['apt.Install("pchar=1.5-2")'])
        self.assertTrue(self.container_run(["sh", "-c", "pchar -V 2>&1"]).find("pchar 1.5") != -1)

    def test_multi(self):
        self.stuff(['apt.Install(["pchar=1.5-2", "wirish"])'])
        self.assertTrue(self.container_run(["sh", "-c", "pchar -V 2>&1"]).find("pchar 1.5") != -1)
        self.assertTrue(self.container_run(["ls", "/usr/share/dict/irish"]).strip() == "/usr/share/dict/irish")


class AptKeyTest(fixture.DockerTest):
    def test_add(self):
        self.stuff(['apt.KeyAdd("https://download.01.org/gfx/RPM-GPG-KEY-ilg-3", update=False)'])
        self.assertTrue(self.container_run(["apt-key", "list"]).find("@intel.com") != -1)


class AptSourceListTest(fixture.DockerTest):
    def test_add(self):
        self.stuff(['apt.SourceList("docker", "deb https://apt.dockerproject.org/repo ubuntu-wily main\\n")'])
        self.assertTrue(self.container_run(['ls', '/var/lib/apt/lists']).find('dockerproject') != -1)

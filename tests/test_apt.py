import sys

from pathlib import Path


sys.path.append(str(Path(__file__).parents[1]))

import fixture


class AptInstallTest(fixture.DockerTest):
    def test_basic(self):
        self.stuff(['apt.Install("pchar=1.5-2")'])
        self.assertTrue(self.container_run(["sh", "-c", "pchar -V 2>&1"]).find("pchar 1.5") != -1)

    def test_multi(self):
        self.stuff(['apt.Install(["pchar=1.5-2", "wirish"])'])
        self.assertTrue(self.container_run(["sh", "-c", "pchar -V 2>&1"]).find("pchar 1.5") != -1)
        self.assertTrue(self.container_run(["ls", "/usr/share/dict/irish"]).strip() == "/usr/share/dict/irish")


class AptPurgeTest(fixture.DockerTest):
    def test_purge(self):
        self.stuff(['apt.Purge("manpages")'])
        self.assertRegex(self.container_run(["sh", "-c", "test -f /usr/share/man/man7/man.7.gz || echo Gone"]), r'Gone')


class AptKeyTest(fixture.DockerTest):
    def test_add(self):
        self.stuff(['apt.KeyAdd("https://download.01.org/gfx/RPM-GPG-KEY-ilg-3")'])
        self.assertTrue(self.container_run(["apt-key", "list"]).find("@intel.com") != -1)

    def test_recv(self):
        self.stuff(['apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "BBEBDCB318AD50EC6865090613B00F1FD2C19886")'])
        self.assertTrue(self.container_run(["apt-key", "list"]).find("@spotify.com") != -1)


class AptSourceListTest(fixture.DockerTest):
    def test_add(self):
        self.stuff(['apt.SourceList("spotify", "deb http://repository.spotify.com stable non-free")'])
        self.stuff(['apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "BBEBDCB318AD50EC6865090613B00F1FD2C19886")'])
        self.stuff(['apt.Install(["xdg-utils", "spotify-client"])'])


class AptAddRepositoryTest(fixture.DockerTest):
    def test_add_repo(self):
        self.stuff(['apt.AddRepository("ppa:webupd8team/java")'])
        self.assertTrue(self.container_run(["ls", "/etc/apt/sources.list.d"]).find("webupd8team") != -1)

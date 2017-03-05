import os
import sys

import re

sys.path.append("{}/..".format(os.path.dirname(__file__)))

import fixture


class FileChmodTest(fixture.DockerTest):
    def test_chmod_600(self):
        self.stuff(['files.Chmod(0o600, "/usr/share/common-licenses/GPL-2")'])
        self.assertTrue(re.search(r"-rw------- ",
                                  self.container_run(
                                      ["ls", "-l", "/usr/share/common-licenses/GPL-2"])))


class FileChownTest(fixture.DockerTest):
    def test_chown(self):
        self.stuff(['files.Chown("games", "/usr/share/common-licenses/GPL-2")'])
        self.assertTrue(re.search(r" games ",
                                  self.container_run(
                                      ["ls", "-l", "/usr/share/common-licenses/GPL-2"])))

    def test_chown_r(self):
        self.stuff(['files.Chown("games", "/usr/share/common-licenses", recursive=True)'])
        self.assertTrue(re.search(r" games ",
                                  self.container_run(
                                      ["ls", "-l", "/usr/share/common-licenses/GPL-3"])))


class FileContentTest(fixture.DockerTest):
    def test_basic(self):
        self.stuff(['files.Content("/tmp/content_test", "test_content\\n")'])
        self.assertEquals(self.container_run(["cat", "/tmp/content_test"]),
                          "test_content\n")

    def test_dynamic(self):
        self.stuff(['files.Content("/tmp/stuffit.py", '
                    '"import subprocess\\n'
                    "files.Content('/tmp/dyn.sh', "
                    "'echo Uname: ' + subprocess.check_output(['uname']).decode())\\n"
                    '")\n'
                    ])
        self.stuff(['--file', '/tmp/stuffit.py'])
        self.assertEquals(self.container_run(["bash", "/tmp/dyn.sh"]), "Uname: Linux\n")

    def test_output_of(self):
        self.stuff(['files.Content("/tmp/output_6.out", content.OutputOf(["echo", "6"]))'])
        self.assertEquals(self.container_run(["cat", "/tmp/output_6.out"]), "6\n")

    def test_output_of_shell(self):
        self.stuff(['files.Content("/tmp/output_5.out", content.OutputOf("echo 5", shell=True))'])
        self.assertEquals(self.container_run(["cat", "/tmp/output_5.out"]), "5\n")


class FileDownloadTest(fixture.DockerTest):
    def test_docker_compose(self):
        self.stuff(['files.DownloadFile("https://github.com/docker/compose/releases/download/1.6.2/'
                    'docker-compose-Linux-x86_64", '
                    '"/usr/local/bin/docker-compose")'])
        self.assertEquals(
            self.container_run(["shasum", "/usr/local/bin/docker-compose"]).split()[0],
            "82129d4e90c7544a52738a570747d653bdb656db")


class FileMkdirTest(fixture.DockerTest):
    def test_mkdir(self):
        self.stuff(['files.Mkdir("/new_dir")'])
        self.assertEquals(self.container_run(["ls", "-d", "/new_dir"]), "/new_dir\n")


class FileTransformTest(fixture.DockerTest):
    def test_basic(self):
        self.stuff(['files.Content("/tmp/transform_test", "old_content\\n")'])
        self.stuff(['files.Transform("/tmp/transform_test", lambda c: c.replace("old", "new"))'])
        self.assertEquals(self.container_run(["cat", "/tmp/transform_test"]), "new_content\n")

    def test_multiline(self):
        """Test that multiline scripts work"""
        self.stuff(['files.Content("/tmp/transform_test", "old_content\\n")',
                    'files.Transform("/tmp/transform_test", lambda c: c.replace("old", "new"))'])
        self.assertEquals(self.container_run(["cat", "/tmp/transform_test"]), "new_content\n")

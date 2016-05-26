import os
import sys


sys.path.append("{}/..".format(os.path.dirname(__file__)))

import fixture


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


class FileTransformTest(fixture.DockerTest):
    def test_basic(self):
        self.stuff(['files.Content("/tmp/transform_test", "old_content\\n")'])
        self.stuff(['files.Transform("/tmp/transform_test", lambda c: c.replace("old", "new"))'])
        self.assertEquals(self.container_run(["cat", "/tmp/transform_test"]), "new_content\n")

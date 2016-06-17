import logging
import os
import shlex
import shutil
import sys
import unittest
from pathlib import Path

from click.testing import CliRunner

from stuffer import main
from stuffer.core import run_cmd
from stuffer.utils import str_split


TEST_IMAGE = "stuffer_test_image"
TEST_CONTAINER = "stuffer_test_ctr"


class DockerTest(unittest.TestCase):
    RUN_LOCAL = False  # True is useful for interactive debugging.

    def setUp(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-7s %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S')
        self.remove_container()
        src_dir = Path(__file__).parents[1].resolve()
        os.system(" ".join(["docker", "build", "--tag", TEST_IMAGE, str(src_dir)]))
        run_cmd(["docker", "run", "--detach", "--name", TEST_CONTAINER,
                 "--volume={}:/stuffer_src".format(str(src_dir)), TEST_IMAGE, "sleep", "10000000"])
        run_cmd(["docker", "exec", TEST_CONTAINER, "./setup.py", "sdist"])
        run_cmd(["docker", "exec", TEST_CONTAINER, "pip3", "install", "./dist/stuffer-0.1.tar.gz"])

    def tearDown(self):
        pass
        # self.remove_container()
        # self.remove_image()

    def remove_container(self):
        if run_cmd(["docker", "ps", "--all", "--quiet", "--filter", "name={}".format(TEST_CONTAINER)]) != "":
            run_cmd(["docker", "rm", "--force", TEST_CONTAINER])

    def remove_image(self):
        if run_cmd(["docker", "images", "--quiet", TEST_IMAGE]) != "":
            run_cmd(["docker", "rmi", "--force", TEST_IMAGE])

    def stuff(self, commands):
        stuffer_store = "/tmp/stuffer_test_store"
        full_commands = ["--conf-store", ("directory: %s" % stuffer_store)] + commands
        if self.RUN_LOCAL:
            shutil.rmtree(stuffer_store, ignore_errors=True)
            return self._stuff_locally(full_commands)
        return self.container_run(["stuffer"] + full_commands
                                  )

    def _stuff_locally(self, commands):
        runner = CliRunner()
        logging.info("> stuffer {}".format(" ".join([shlex.quote(c) for c in commands])))
        result = runner.invoke(main.cli, commands, catch_exceptions=False)
        if result.exit_code != 0:
            logging.error(result.output)
        else:
            logging.debug(result.output)
        assert result.exit_code == 0
        return result.output

    def container_run(self, commands):
        return run_cmd(["docker", "exec", "--tty=false", TEST_CONTAINER] + str_split(commands))

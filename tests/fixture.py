import logging
import os
import re
import sys
import unittest

from click.testing import CliRunner

from stuffer import main
from stuffer.core import run_cmd


TEST_IMAGE = "stuffer_test_image"
TEST_CONTAINER = "stuffer_test_ctr"


class DockerTest(unittest.TestCase):
    RUN_LOCAL = False

    def setUp(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-7s %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S')
        self.remove_container()
        os.system(" ".join(["docker", "build", "--tag", TEST_IMAGE, "{}/..".format(os.path.dirname(__file__))]))
        run_cmd(["docker", "run", "--detach", "--name", TEST_CONTAINER, TEST_IMAGE, "sleep", "10000000"])
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
        if self.RUN_LOCAL:
            runner = CliRunner()
            logging.info("> stuffer --dry-run {}".format(" ".join(commands)))
            result = runner.invoke(main.cli, ["--dry-run"] + commands, catch_exceptions=False)
            if result.exit_code != 0:
                logging.error(result.output)
            else:
                logging.debug(result.output)
            assert result.exit_code == 0
            return result.output
        return self.container_run(["stuffer"] + commands)

    def stuff_all_from(self, path):
        """Run all commands in a file. Avoid the alternative --file, in order to use Docker cache."""
        script = main.script_substance(main.command_script(path, None))
        # This will join lines that start with whitespace into previous line.
        blocks = re.findall(r".*?\n\b", script, re.DOTALL)
        for block in blocks:
            self.stuff([block])

    def container_run(self, commands):
        return run_cmd(["docker", "exec", "--tty", TEST_CONTAINER] + commands)

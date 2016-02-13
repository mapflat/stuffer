#! /usr/bin/env python

import logging
import os
import subprocess
import sys
import unittest

from click.testing import CliRunner


sys.path.append("{}/..".format(os.path.dirname(__file__)))

from stuffer import main


TEST_IMAGE = "stuffer_test_image"
TEST_CONTAINER = "stuffer_test_ctr"


def run_cmd(cmd, *args, **kwargs):
    logging.info("> {}".format(" ".join(cmd)))
    try:
        out = subprocess.check_output(cmd, *args, **kwargs)
    except subprocess.CalledProcessError as err:
        logging.error("Command failed:\n{}".format(err.output))
        raise
    logging.debug(out)
    return out


class DockerTest(unittest.TestCase):
    RUN_LOCAL = False

    def setUp(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.remove_container()
        os.system(" ".join(["docker", "build", "--tag", TEST_IMAGE, "{}/..".format(os.path.dirname(__file__))]))
        run_cmd(["docker", "run", "--detach", "--name", TEST_CONTAINER, TEST_IMAGE, "sleep", "10000000"])
        run_cmd(["docker", "exec", TEST_CONTAINER, "./setup.py", "sdist"])
        run_cmd(["docker", "exec", TEST_CONTAINER, "pip", "install", "./dist/stuffer-0.1.tar.gz"])

    def tearDown(self):
        pass
        # self.remove_container()
        # self.remove_image()

    def remove_container(self):
        if run_cmd(["docker", "ps", "--quiet", "--filter", "name={}".format(TEST_CONTAINER)]) != "":
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
        return self.ctr_run(["stuffer"] + commands)

    def ctr_run(self, commands):
        return run_cmd(["docker", "exec", "--tty", TEST_CONTAINER] + commands)


class AptInstallTest(DockerTest):
    def test_basic_install(self):
        self.stuff(['apt.Install("pchar=1.5-2")'])
        self.assert_(self.ctr_run(["pchar", "-V"]).find("pchar 1.5") != -1)

import abc
import logging
import subprocess

from pathlib import Path

from stuffer.utils import NaturalReprMixin, str_split


class Action(NaturalReprMixin):
    """Base class for all actions to be taken."""

    __metaclass__ = abc.ABCMeta

    _registry = []

    @classmethod
    def registered(cls):
        return list(cls._registry)

    def __init__(self):
        self._registry.append(self)
        logging.debug("Registered action: {}".format(self))

    def execute(self):
        logging.info("Executing {}".format(self))
        for prereq in self.prerequisites():
            prereq.run()
        self.run()

    def prerequisites(self):
        return []

    def command(self):
        pass

    def use_shell(self):
        return False

    @staticmethod
    def tmp_dir():
        return Path("/tmp/stuffer_tmp")

    def run(self):
        cmd = self.command() if self.use_shell() else str_split(self.command())
        return run_cmd(cmd, shell=self.use_shell())


def run_cmd(cmd, *args, **kwargs):
    verbose = kwargs.pop('verbose', False)
    joined = " ".join(str_split(cmd))
    logging.info("> %s", joined)
    try:
        output = subprocess.check_output(cmd, *args, **kwargs).decode()
        if verbose:
            logging.info(output)
        else:
            logging.debug(output)
        return output
    except subprocess.CalledProcessError as err:
        logging.error("Command %s failed:\n%s", joined, str(err.output))
        raise

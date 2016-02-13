import logging

import abc
import subprocess

from stuffer.utils import NaturalReprMixin


class Action(NaturalReprMixin):
    """Base class for all actions to be taken."""

    __metaclass__ = abc.ABCMeta

    _registry = set()

    @classmethod
    def registered(cls):
        return list(cls._registry)

    def __init__(self):
        self._registry.add(self)

    def execute(self, dry_run):
        logging.info("Executing {}".format(self))
        self.run(dry_run)

    @abc.abstractmethod
    def command(self):
        raise NotImplementedError()

    def run(self, dry_run):
        logging.info("> {}".format(self.command()))
        cmd = self.split(self.command())
        if not dry_run:
            try:
                output = subprocess.check_output(cmd)
                logging.info(output)
            except subprocess.CalledProcessError as err:
                logging.exception("Command failed: {}\n{}".format(cmd, err.output))
                raise

    def split(self, cmd):
        if isinstance(cmd, str):
            return cmd.split()
        return cmd

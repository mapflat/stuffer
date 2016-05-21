import abc
import logging
import subprocess

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

    def execute(self, dry_run):
        logging.info("Executing {}".format(self))
        for prereq in self.prerequisites():
            prereq.run(dry_run)
        self.run(dry_run)

    def prerequisites(self):
        return []

    @abc.abstractmethod
    def command(self):
        raise NotImplementedError()

    def use_shell(self):
        return False

    def run(self, dry_run):
        cmd = self.command() if self.use_shell() else str_split(self.command())
        return run_cmd(cmd, dry_run=dry_run, shell=self.use_shell())


def run_cmd(cmd, *args, **kwargs):
    dry_run = kwargs.pop('dry_run', False)
    verbose = kwargs.pop('verbose', False)
    joined = " ".join(cmd)
    logging.info("> %s", joined)
    if not dry_run:
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

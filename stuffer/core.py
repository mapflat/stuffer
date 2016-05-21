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
        self.run(dry_run)

    @abc.abstractmethod
    def command(self):
        raise NotImplementedError()

    def run(self, dry_run):
        return run_cmd(str_split(self.command()), dry_run=dry_run)


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

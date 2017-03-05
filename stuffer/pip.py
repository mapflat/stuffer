from .core import Action
from . import apt


class Install(Action):
    """Install a package with pip install."""

    def __init__(self, package, upgrade=False):
        self.package = package
        self.upgrade = upgrade
        super(Install, self).__init__()

    def prerequisites(self):
        return [apt.Install(["python3-pip"], update=False)]

    def command(self):
        return "pip3 install {}{}".format("--upgrade " if self.upgrade else "", self.package)

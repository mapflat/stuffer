from .core import Action
from . import apt


class Install(Action):
    """Install a package with pip install."""

    def __init__(self, package):
        self.package = package
        super(Install, self).__init__()

    def prerequisites(self):
        return [apt.Install(["python3-pip"])]	

    def command(self):
        return "pip3 install {}".format(self.package)

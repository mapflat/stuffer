from .core import Action


class Install(Action):
    """Install a package with apt-get install."""

    def __init__(self, package):
        super(Install, self).__init__()
        self.package = package

    def command(self):
        return "apt-get install --yes {}".format(self.package)

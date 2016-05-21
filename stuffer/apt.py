from .core import Action


class Install(Action):
    """Install a package with apt-get install."""

    def __init__(self, package):
        self.packages = [package] if isinstance(package, str) else list(package)
        super(Install, self).__init__()

    def command(self):
        return "apt-get install --yes {}".format(" ".join(self.packages))

from .core import Action


class Install(Action):
    """Install a package with apt-get install."""

    def __init__(self, package):
        self.packages = [package] if isinstance(package, str) else list(package)
        super(Install, self).__init__()

    def command(self):
        return "apt-get install --yes {}".format(" ".join(self.packages))


class KeyAdd(Action):
    """Add a trusted key to apt."""

    def __init__(self, url):
        self.url = url
        super(KeyAdd, self).__init__()

    def prerequisites(self):
        return [Install('wget')]

    def use_shell(self):
        return True

    def command(self):
        return "wget {} -O - | apt-key add -".format(self.url)

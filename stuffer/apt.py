from pathlib import Path

from stuffer import content
from stuffer.files import write_file_atomically
from .core import Action, run_cmd


class Install(Action):
    """Install a package with apt-get install."""

    def __init__(self, package, update_first=False):
        self.packages = [package] if isinstance(package, str) else list(package)
        self.update_first = update_first
        super(Install, self).__init__()

    def run(self):
        if self.update_first:
           run_cmd(["apt-get", "update"])
        run_cmd(["apt-get", "install", "--yes"] + self.packages)


class KeyAdd(Action):
    """Add a trusted key to apt using apt-key add method."""

    def __init__(self, url):
        self.url = url
        super(KeyAdd, self).__init__()

    def prerequisites(self):
        return [Install('wget')]

    def run(self):
        run_cmd("wget {} -O - | apt-key add -".format(self.url), shell=True)


class KeyRecv(Action):
    """Add a trusted key to apt using apt-key --recv-keys method."""

    def __init__(self, keyserver, key):
        self.keyserver = keyserver
        self.key = key
        super(KeyRecv, self).__init__()

    def command(self):
        return "apt-key adv  --keyserver {} --recv-keys {}".format(self.keyserver, self.key)


class SourceList(Action):
    def __init__(self, name, contents):
        self.name = name
        self.contents = content.supplier(contents)
        super(SourceList, self).__init__()

    def prerequisites(self):
        return [Install('apt-transport-https')]

    def run(self):
        write_file_atomically(Path("/etc/apt/sources.list.d").joinpath(self.name).with_suffix(".list"),
                              self.contents())

from pathlib import Path

from stuffer import content
from stuffer.files import write_file_atomically
from .core import Action, run_cmd


class Install(Action):
    """Install a package with apt-get install."""

    def __init__(self, package):
        self.packages = [package] if isinstance(package, str) else list(package)
        super(Install, self).__init__()

    def command(self):
        return "apt-get install --yes {}".format(" ".join(self.packages))


class KeyAdd(Action):
    """Add a trusted key to apt."""

    def __init__(self, url, update=True):
        self.url = url
        self.update = update
        super(KeyAdd, self).__init__()

    def prerequisites(self):
        return [Install('wget')]

    def run(self):
        run_cmd("wget {} -O - | apt-key add -".format(self.url), shell=True)
        if self.update:
            Update().run()


class Update(Action):
    """Run apt-get update."""

    def command(self):
        return "apt-get update"


class SourceList(Action):
    def __init__(self, name, contents, update=True):
        self.name = name
        self.contents = content.supplier(contents)
        self.update = update
        super(SourceList, self).__init__()

    def prerequisites(self):
        return [Install('apt-transport-https')]

    def run(self):
        write_file_atomically(Path("/etc/apt/sources.list.d").joinpath(self.name).with_suffix(".list"),
                              self.contents())
        if self.update:
            Update().run()

import shutil
import urllib.request
from pathlib import Path

from stuffer import content
from stuffer.core import Action


class Chmod(Action):
    """Set permissions for a file."""

    def __init__(self, permissions, path):
        self.permissions = permissions
        self.path = Path(path)
        super().__init__()

    def command(self):
        return "chmod {:o} {}".format(self.permissions, str(self.path))


class Content(Action):
    """Set the contents of a file."""

    def __init__(self, path, contents):
        self.path = Path(path)
        self.contents = content.supplier(contents)
        super(Content, self).__init__()

    def run(self):
        write_file_atomically(self.path, self.contents())


class DownloadFile(Action):
    """Download and install a single file from a URL."""

    def __init__(self, url, path):
        self.url = url
        self.path = Path(path)
        super().__init__()

    def run(self):
        local_file, _ = urllib.request.urlretrieve(self.url)
        shutil.move(local_file, str(self.path))


class Mkdir(Action):
    """Create a directory, unless it exists."""

    def __init__(self, path):
        self.path = path
        super().__init__()

    def command(self):
        return "mkdir -p {}".format(self.path)


class Transform(Action):
    """Transform the contents of a file"""

    def __init__(self, path, transform):
        self.path = Path(path)
        self.transform = transform
        super(Transform, self).__init__()

    def run(self):
        with self.path.open() as f:
            new_content = self.transform(f.read())
        write_file_atomically(self.path, new_content)


def write_file_atomically(path, contents, suffix=".stuffer_tmp"):
    tmp_file = path.with_suffix(path.suffix + suffix)
    with tmp_file.open('w') as tmp:
        tmp.write(contents)
    try:
        tmp_file.replace(path)
    except:
        if path.exists() and tmp_file.exists():
            tmp_file.unlink()
        raise

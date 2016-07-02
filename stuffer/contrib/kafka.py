from pathlib import Path

from stuffer import apt
from stuffer.core import Action


class Kafka(Action):
    def __init__(self, version, scala_version='2.11', destination='/opt/kafka'):
        self.version = version
        self.scala_version = scala_version
        self.destination = Path(destination)
        super().__init__()

    def prerequisites(self):
        return [apt.Install('wget')]

    def run(self):
        self._extract_net_archive('http://apache.mirrors.spacedump.net/kafka/{}/kafka_{}-{}.tgz'.format(
            self.version, self.scala_version, self.version),
            self.destination)

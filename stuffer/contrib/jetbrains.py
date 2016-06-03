import logging
from pathlib import Path

from stuffer import apt
from stuffer.core import Action, run_cmd


class IntelliJ(Action):
    def __init__(self, version, build, variant="IC", destination="/usr/local"):
        self.version = version
        self.build = build
        self.variant = variant
        self.destination = Path(destination)
        super(IntelliJ, self).__init__()

    def prerequisites(self):
        return [apt.Install(["wget"])]

    def run(self):
        tar_file_name = "idea{}-{}.tar.gz".format(self.variant, self.version)
        idea_dest = self.destination.joinpath("idea-{}-{}".format(self.variant, self.build))
        if not idea_dest.is_dir():
            logging.info("Installing idea%s-%s", self.variant, self.version)
            if not self.destination.is_dir():
                self.destination.mkdir(parents=True, exist_ok=True)
            local_tar = self.tmp_dir().joinpath(tar_file_name)
            if not local_tar.exists():
                tar_url = 'http://download.jetbrains.com/idea/{}'.format(tar_file_name)
                run_cmd(["wget", "--quiet", "--output-document", str(local_tar), tar_url])
            run_cmd(["tar", "--directory", str(self.destination), "-xf", str(local_tar)])

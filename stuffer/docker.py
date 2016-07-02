import logging
from pathlib import Path

from stuffer.core import Action


class Prologue(Action):
    def run(self):
        if not Path('/etc/my_init.d').is_dir():
            logging.warning("This does not seem to be an image derived from phusion/baseimage. "
                            "It is recommended to use an image adapted for Docker")


class Epilogue(Action):
    def use_shell(self):
        return True

    def command(self):
        return "apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*"

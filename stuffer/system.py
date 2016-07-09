import getpass
import os


def real_user():
    return os.environ.get('SUDO_USER', getpass.getuser())


from stuffer.configuration import config
from .core import Action


class StoreAction(Action):
    @staticmethod
    def store_dir():
        return config.store_directory

    def create_store_dir(self):
        self.store_dir().mkdir(parents=True, exist_ok=True)

    @staticmethod
    def key_path(key):
        return StoreAction.store_dir().joinpath(key)


class Set(StoreAction):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        super().__init__()

    def run(self):
        self.create_store_dir()
        self.key_path(self.key).write_text(self.value)


def get(key):
    if StoreAction.key_path(key).exists():
        return StoreAction.key_path(key).read_text()

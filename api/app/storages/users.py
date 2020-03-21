import shelve
import logging

from typing import Optional

from config import USERS_DB_FILE_PATH


logger = logging.getLogger(__name__)


class ShelveUsersStorage(object):
    def __init__(self, filepath: str):
        self._data: shelve.Shelf = shelve.open(filepath)

    def get_user(self, username, password):
        pass

    def create_user(self, username, password):
        pass


_user_storage: Optional[ShelveUsersStorage]


def initialize_users_storage():
    global _user_storage
    _user_storage = ShelveUsersStorage(USERS_DB_FILE_PATH)
    logger.info('Initialized Users Storage')


def get_users_storage() -> ShelveUsersStorage:
    if _user_storage is None:
        raise RuntimeError('Users Storage is not initialized')
    return _user_storage

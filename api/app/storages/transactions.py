import json
import logging

from typing import List, Optional

from config import DATASET_FILE_PATH
from models import Transaction


logger = logging.getLogger(__name__)


class InMemoryTransactionsStorage(object):
    def __init__(self, data: List[Transaction]):
        self._data: List[Transaction] = data

    def list_transactions(
            self, offset: int = 0, limit: int = None,
    ) -> List[Transaction]:
        if limit is not None:
            return self._data[offset:offset + limit]
        return self._data[offset:]

    def count_transactions(self):
        return len(self._data)


_transactions_storage: Optional[InMemoryTransactionsStorage]


def initialize_transactions_storage():
    global _transactions_storage

    with open(DATASET_FILE_PATH) as json_file:
        data = json.load(json_file)

    _transactions_storage = InMemoryTransactionsStorage(
        [Transaction(**tx) for tx in data]
    )
    logger.info('Initialized Transactions Storage')


def get_transactions_storage() -> InMemoryTransactionsStorage:
    if _transactions_storage is None:
        raise RuntimeError('Transactions storage is not initialized')
    return _transactions_storage

from typing import Tuple, Any

from factory.random import randgen

from .constants import AttachmentFormat, Direction, TransactionType


class Distribution(dict):
    """Value->Probability pairs"""

    def __init__(self, *distributions: Tuple[Any, int]):
        super(Distribution, self).__init__(distributions)
        if sum(self.values()) != 100:
            raise AttributeError(
                f'Sum of weights = {sum(self.values())}, must sum up to 100')

    def weights(self):
        return list(self.values())

    def population(self):
        return list(self.keys())

    def flip(self):
        return randgen.choices(
            population=self.population(),
            weights=self.weights(),
            k=1,
        )[0]


ATTACHMENT_FORMAT = Distribution(
    (AttachmentFormat.PDF, 25),
    (AttachmentFormat.JPG, 55),
    (AttachmentFormat.PNG, 15),
    (AttachmentFormat.GIF, 5),
)
ATTACHMENT_ACTIVE = Distribution(
    (True, 80),
    (False, 20),
)

ATTACHMENT_COUNT_PER_TRANSACTION = Distribution(
    (0, 30),
    (1, 50),
    (2, 10),
    (3, 5),
    (4, 5),
)

_ONE_HOUR = 3600 # sec
ATTACHMENT_ADDED_SECONDS_AFTER_TRANSACTION_TIER = Distribution(
    ((1, 9), 10),
    ((10, 60), 20),
    ((61, 300), 15),
    ((301, _ONE_HOUR), 15),
    ((_ONE_HOUR * 10 + 1, _ONE_HOUR * 24), 25),
    ((_ONE_HOUR * 24 + 1, _ONE_HOUR * 24 * 30), 15),
)

TRANSACTION_DIRECTION = Distribution(
    (Direction.IN, 60),
    (Direction.OUT, 40),
)

TRANSACTION_TYPE = Distribution(
    (TransactionType.Card, 45),
    (TransactionType.BankTransfer, 35),
    (TransactionType.TopUp, 15),
    (TransactionType.OnlineStorePurchase, 5),
)

TRANSACTIONS_PER_ACCOUNT_TIER = Distribution(
    ((0, 0), 5),  # not transacting accounts
    ((1, 5), 25),
    ((6, 15), 35),
    ((16, 25), 20),
    ((25, 40), 10),
    ((41, 70), 5),
)

TRANSACTIONS_AMOUNT_TIER = Distribution(
    ((1, 10), 5),
    ((11, 50), 20),
    ((51, 150), 30),
    ((151, 500), 20),
    ((501, 2000), 10),
    ((2001, 5000), 10),
    ((5000, 15000), 5),
)

ACCOUNT_CREATE_YEAR_MONTH = Distribution(
    ((2019, 1), 2),
    ((2019, 2), 2),
    ((2019, 3), 3),
    ((2019, 4), 3),
    ((2019, 5), 5),
    ((2019, 6), 5),
    ((2019, 7), 8),
    ((2019, 8), 9),
    ((2019, 9), 12),
    ((2019, 10), 12),
    ((2019, 11), 18),
    ((2019, 12), 21),
    # END_DATE = 2020-01-01
)

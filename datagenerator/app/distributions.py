from typing import Tuple, Any

from factory.random import randgen

from .constants import (
    AttachmentFormat, Direction, TransactionType,
    CategoryIn, CategoryOut, VatRate,
)


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

_ONE_HOUR = 3600  # sec
ATTACHMENT_ADDED_SECONDS_AFTER_TRANSACTION_TIER = Distribution(
    ((1, 9), 10),
    ((10, 60), 20),
    ((61, 300), 15),
    ((301, _ONE_HOUR), 15),
    ((_ONE_HOUR * 10 + 1, _ONE_HOUR * 24), 25),
    ((_ONE_HOUR * 24 + 1, _ONE_HOUR * 24 * 30), 15),
)

CATEGORY_ADDED_SECONDS_AFTER_TRANSACTION_TIER = Distribution(
    ((1, 9), 20),
    ((10, 60), 30),
    ((61, 300), 25),
    ((31, _ONE_HOUR * 24), 25),
)

TRANSACTION_DIRECTION = Distribution(
    (Direction.IN, 40),
    (Direction.OUT, 60),
)

TRANSACTION_TYPE_OUT = Distribution(
    (TransactionType.Card, 70),
    (TransactionType.BankTransfer, 30),
)

TRANSACTION_TYPE_IN = Distribution(
    (TransactionType.BankTransfer, 60),
    (TransactionType.TopUp, 22),
    (TransactionType.Card, 3),  # card refunds
    (TransactionType.OnlineStorePurchase, 15),
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

CATEGORY_OUT = Distribution(
    (CategoryOut.GeneralExpense, 13),
    (CategoryOut.Office, 12),
    (CategoryOut.Personal, 12),
    (CategoryOut.Contract, 8),
    (CategoryOut.Telecom, 8),
    (CategoryOut.Tax, 8),
    (CategoryOut.Salary, 6),
    (CategoryOut.MealsEntertainment, 5),
    (CategoryOut.Marketing, 5),
    (CategoryOut.Insurance, 4),
    (CategoryOut.Rent, 4),
    ((None, None), 15),
)

CATEGORY_IN = Distribution(
    (CategoryIn.GeneralIncome, 50),
    (CategoryIn.Personal, 30),
    ((None, None), 20),
)

VAT_RATE = Distribution(
    (VatRate.P0, 40),
    (VatRate.P10, 6),
    (VatRate.P14, 4),
    (VatRate.P24, 30),
    (None, 20),
)

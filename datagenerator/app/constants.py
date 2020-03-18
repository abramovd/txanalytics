import datetime

from collections import namedtuple

START_DATE = datetime.datetime(
    year=2018, month=1, day=1,
    tzinfo=datetime.timezone.utc,
)
END_DATE = datetime.datetime(
    year=2020, month=3, day=1,
    tzinfo=datetime.timezone.utc,
)

AttachmentFormat = namedtuple(
    'AttachmentFormat',
    ['PDF', 'JPG', 'PNG', 'GIF'],
)(
    PDF='pdf',
    JPG='jpg',
    PNG='png',
    GIF='gif',
)

Direction = namedtuple(
    'Direction',
    ['IN', 'OUT'],
)(
    IN='in',
    OUT='out',
)
TransactionType = namedtuple(
    'TransactionType',
    ['Card', 'BankTransfer', 'TopUp', 'OnlineStorePurchase']
)(
    Card='card',
    BankTransfer='bank_transfer',
    TopUp='top_up',
    OnlineStorePurchase='online_store_purchase',
)

NUM_ACCOUNTS = 100

import datetime
import uuid

from collections import namedtuple

END_DATE = datetime.datetime(
    year=2020, month=1, day=1,
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

DEFAULT_NUM_ACCOUNTS = 100
DEFAULT_RANDOM_SEED = 123
Output = namedtuple(
    'Output',
    ['Stdout', 'Dump'],
)(
    Stdout='stdout',
    Dump='dump',
)

CategoryOut = namedtuple(
    'CategoryOut',
    [
        'Office', 'Personal', 'Contract', 'Telecom', 'Tax',
        'Salary', 'MealsEntertainment', 'Marketing', 'Insurance',
        'Rent', 'GeneralExpense',
    ]
)(
    Office=(uuid.uuid4(), 'Office Supplies'),
    Personal=(uuid.uuid4(), 'Personal Withdrawals'),
    Contract=(uuid.uuid4(), 'Contract Services'),
    Telecom=(uuid.uuid4(), 'Telecommunication'),
    Tax=(uuid.uuid4(), 'Taxes'),
    Salary=(uuid.uuid4(), 'Salary'),
    MealsEntertainment=(uuid.uuid4(),'Meals & Entertainment'),
    Marketing=(uuid.uuid4(), 'Marketing'),
    Insurance=(uuid.uuid4(), 'Insurance'),
    Rent=(uuid.uuid4(), 'Rent'),
    GeneralExpense=(uuid.uuid4(), 'General Expense'),
)
CategoryIn = namedtuple(
    'CategoryIn',
    [
        'GeneralIncome', 'Personal'
    ]
)(
    GeneralIncome=(uuid.uuid4(), 'General Income'),
    Personal=(uuid.uuid4(), 'Personal'),
)

VatRate = namedtuple(
    'VatRate',
    [
        'P10', 'P14', 'P24', 'P0'
    ]
)(
    P10='10%',
    P14='14%',
    P24='24%',
    P0='0%,'

)

import uuid
import factory

from datetime import timedelta
from factory.fuzzy import FuzzyDateTime, FuzzyDecimal, FuzzyInteger

from .fuzzy import FuzzyDistributedChoice
from .models import (
    Attachment, Category, Account, Transaction,
)
from .constants import START_DATE, END_DATE
from .distributions import (
    ATTACHMENT_FORMAT, ATTACHMENT_ACTIVE,
    TRANSACTION_DIRECTION, TRANSACTION_TYPE,
    TRANSACTIONS_AMOUNT_TIER,
    ATTACHMENT_ADDED_SECONDS_AFTER_TRANSACTION_TIER,
)


def get_attachment_added_at(transaction: Transaction):
    low_sec, high_sec = \
        ATTACHMENT_ADDED_SECONDS_AFTER_TRANSACTION_TIER.flip()
    seconds = FuzzyInteger(low_sec, high_sec).fuzz()
    return FuzzyDateTime(
        start_dt=transaction.timestamp,
        end_dt=transaction.timestamp + timedelta(seconds=seconds)
    )


class AttachmentFactory(factory.Factory):
    class Meta:
        model = Attachment

    id = factory.LazyFunction(uuid.uuid4)
    format = FuzzyDistributedChoice(
        distribution=ATTACHMENT_FORMAT,
    )
    active = FuzzyDistributedChoice(
        distribution=ATTACHMENT_ACTIVE,
    )


class AccountFactory(factory.Factory):
    class Meta:
        model = Account

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker('company')
    created_at = FuzzyDateTime(start_dt=START_DATE, end_dt=END_DATE)


def get_transaction_amount():
    low, high = TRANSACTIONS_AMOUNT_TIER.flip()
    return FuzzyDecimal(low=low, high=high).fuzz()


class TransactionFactory(factory.Factory):
    class Meta:
        model = Transaction

    id = factory.LazyFunction(uuid.uuid4)
    amount = factory.LazyFunction(get_transaction_amount)
    timestamp = factory.LazyAttribute(
        lambda o: FuzzyDateTime(
            start_dt=o.account.created_at, end_dt=END_DATE).fuzz()
    )
    direction = FuzzyDistributedChoice(TRANSACTION_DIRECTION)
    type = FuzzyDistributedChoice(TRANSACTION_TYPE)

    # TODO: vat_rate, category

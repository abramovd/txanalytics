import uuid
import datetime
import factory

from decimal import Decimal

from dateutil.relativedelta import relativedelta
from factory.fuzzy import FuzzyDateTime, FuzzyDecimal, FuzzyInteger

from .fuzzy import FuzzyDistributedChoice
from .models import (
    Attachment, Category, Account, Transaction,
)
from .constants import END_DATE, Direction
from .distributions import (
    ATTACHMENT_FORMAT, ATTACHMENT_ACTIVE,
    TRANSACTION_DIRECTION, TRANSACTION_TYPE,
    TRANSACTIONS_AMOUNT_TIER,
    ATTACHMENT_ADDED_SECONDS_AFTER_TRANSACTION_TIER,
    ATTACHMENT_COUNT_PER_TRANSACTION,
    ACCOUNT_CREATE_YEAR_MONTH,
)


def get_attachment_added_at(transaction: Transaction) -> datetime.datetime:
    low_sec, high_sec = \
        ATTACHMENT_ADDED_SECONDS_AFTER_TRANSACTION_TIER.flip()
    seconds = FuzzyInteger(low_sec, high_sec).fuzz()
    return FuzzyDateTime(
        start_dt=transaction.timestamp,
        end_dt=transaction.timestamp + datetime.timedelta(seconds=seconds)
    ).fuzz()


def get_account_created_at() -> datetime.datetime:
    year, month = ACCOUNT_CREATE_YEAR_MONTH.flip()
    start_dt = datetime.datetime(
        year=year, month=month, day=1,
        tzinfo=datetime.timezone.utc,
    )
    return FuzzyDateTime(
        start_dt=start_dt, end_dt=start_dt + relativedelta(months=1)
    ).fuzz()


def get_transaction_amount(force_high=None) -> Decimal:
    low, high = TRANSACTIONS_AMOUNT_TIER.flip()

    force_high = high or force_high
    high = max(high, force_high)
    low = min(low, high)
    return FuzzyDecimal(low=low, high=high).fuzz()


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
    created_at = factory.LazyFunction(get_account_created_at)


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

    # TODO: type and direction should be correlated,
    # e.g. TopUp and OnlineStorePurchase should be only Inbound
    type = FuzzyDistributedChoice(TRANSACTION_TYPE)

    @factory.post_generation
    def generate_attachments(transaction, create, extracted, **kwargs):
        count = ATTACHMENT_COUNT_PER_TRANSACTION.flip()
        attachments = []
        for _ in range(count):
            attachment = AttachmentFactory.build(
                added_at=get_attachment_added_at(transaction),
            )
            attachments.append(attachment)
        transaction.attachments = attachments
        return attachments

    # TODO: vat_rate, category

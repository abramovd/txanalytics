from typing import List

from factory.random import randgen

from .factories import (
    AttachmentFactory, AccountFactory, TransactionFactory,
    get_attachment_added_at,
)
from .constants import NUM_ACCOUNTS
from .models import (
    Attachment, Account, Transaction,
)
from .distributions import (
    ATTACHMENT_COUNT_PER_TRANSACTION,
    TRANSACTIONS_PER_ACCOUNT_TIER,
)


# TODO: move to post generation?
def generate_attachments(for_transaction) -> List[Attachment]:
    count = ATTACHMENT_COUNT_PER_TRANSACTION.flip()
    attachments = []
    for _ in range(count):
        attachment = AttachmentFactory.build(
            added_at=get_attachment_added_at(for_transaction),
        )
        attachments.append(attachment)
    return attachments


def generate_accounts(count) -> List[Account]:
    return AccountFactory.build_batch(count)


def generate_transactions(for_account: Account) -> List[Transaction]:
    count_from, count_to = TRANSACTIONS_PER_ACCOUNT_TIER.flip()
    count = randgen.randint(count_from, count_to)

    transactions = TransactionFactory.build_batch(count, account=for_account)
    for transaction in transactions:
        transaction.attachments = generate_attachments(transaction)

    return transactions


def generate():
    # TODO: dump to datasets based on env variable path
    transactions = []
    accounts = generate_accounts(NUM_ACCOUNTS)
    for account in accounts:
        transactions += generate_transactions(account)

    transactions = sorted(transactions, key=lambda tx: tx.timestamp)
    for transaction in transactions:
        print(transaction.dict())
        print('----')
    print(len(transactions))

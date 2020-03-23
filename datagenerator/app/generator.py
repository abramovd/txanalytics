import json
import os
import datetime
import time
import click

from typing import List

from factory.random import randgen, reseed_random

from .factories import (
    AccountFactory, TransactionFactory,
)
from .constants import Output, Direction
from .models import (
    Account, Transaction,
)
from .distributions import (
    TRANSACTIONS_PER_ACCOUNT_TIER,
)
from .utils import PydanticJSONEncoder


class Generator(object):
    def __init__(self, num_accounts: int, output: str,
                 random_seed: int, dump_path: str,
                 ):
        self.num_accounts = num_accounts
        self.output = output
        self.random_seed = random_seed
        if self.output == Output.Dump:
            self.dump_path = os.path.join(dump_path, self._get_filename())
        else:
            self.dump_path = None

    def _get_filename(self) -> str:
        now_str = datetime.datetime.now().isoformat(timespec='seconds')
        return f'{self.num_accounts}_{self.random_seed}_{now_str}.json'

    @staticmethod
    def generate_accounts(count: int) -> List[Account]:
        for _ in range(count):
            yield AccountFactory.build()

    @staticmethod
    def _adjust_txs_for_balance(account_txs: List[Transaction]):
        balance = 0
        for tx in sorted(account_txs, key=lambda _tx: _tx.timestamp):
            next_balance = balance + (
                tx.amount if tx.direction == Direction.IN
                else -tx.amount
            )

            if tx.direction == Direction.OUT and next_balance < 0:
                assert next_balance == balance - tx.amount
                adjusted_amount = max(balance - 1, 0)
                if adjusted_amount == 0:
                    tx.direction = Direction.IN
                else:
                    tx.amount = adjusted_amount

    def _generate_transactions_for_accounts(
            self, account: Account,
    ) -> List[Transaction]:
        count_from, count_to = TRANSACTIONS_PER_ACCOUNT_TIER.flip()
        count = randgen.randint(count_from, count_to)

        account_transactions = TransactionFactory.build_batch(
            count,
            account=account,
        )
        self._adjust_txs_for_balance(account_txs=account_transactions)
        return account_transactions

    def generate_transactions(
            self, accounts: List[Account],
    ) -> List[Transaction]:
        transactions = []

        with click.progressbar(
                accounts, label='Generating Transactions',
                length=self.num_accounts,
        ) as bar:
            for account in bar:
                transactions += \
                    self._generate_transactions_for_accounts(account)

        return transactions

    def dump_transactions(self, transactions: List[Transaction]) -> None:
        result = json.dumps(
            transactions, indent=4, sort_keys=True, cls=PydanticJSONEncoder,
        )
        if self.output == Output.Stdout:
            print(result)
        elif self.output == Output.Dump:
            with open(self.dump_path, 'w') as f:
                f.write(result)
        else:
            raise ValueError('Not supported output value')

    def _print_summary(self, transactions: List, seconds_spent: float) -> None:
        print('Summary:')
        print(f'Total Accounts: {self.num_accounts}')
        print(f'Total Transactions: {len(transactions)}')
        print(f'Random seed: {self.random_seed}')

        output_value = self.output
        if self.output == Output.Dump:
            output_value += ' to ' + self.dump_path

        print(f'Data output: {output_value}')
        print(f'Time spent: {datetime.timedelta(seconds=seconds_spent)}')

    def run(self, print_summary: bool = True) -> None:
        start_time = time.time()
        reseed_random(self.random_seed)

        accounts = self.generate_accounts(self.num_accounts)

        transactions = self.generate_transactions(accounts)
        transactions = sorted(transactions, key=lambda tx: tx.timestamp)

        self.dump_transactions(transactions)

        end_time = time.time()
        if print_summary:
            self._print_summary(
                transactions, seconds_spent=end_time - start_time,
            )

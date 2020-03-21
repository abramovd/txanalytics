import click
import os

from .generator import Generator
from .constants import DEFAULT_NUM_ACCOUNTS, DEFAULT_RANDOM_SEED, Output


@click.command()
@click.option(
    '--num-accounts', default=DEFAULT_NUM_ACCOUNTS, show_default=True,
    type=click.INT,
)
@click.option(
    '--random-seed', default=DEFAULT_RANDOM_SEED, show_default=True,
    type=click.INT,
)
@click.option(
    '--output', default=Output.Stdout, show_default=True,
    type=click.Choice([Output.Stdout, Output.Dump]),
)
@click.option(
    '--dump_path', default=os.environ.get('DATASETS_DIR', '/datasets/'),
    show_default=True, type=click.Path(),
)
def handle(num_accounts, random_seed, output, dump_path):
    generator = Generator(
        num_accounts=num_accounts, output=output,
        random_seed=random_seed, dump_path=dump_path,
    )
    generator.run()


if __name__ == '__main__':
    handle()


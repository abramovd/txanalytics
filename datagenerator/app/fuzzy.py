from factory.fuzzy import BaseFuzzyAttribute

from .distributions import Distribution


class FuzzyDistributedChoice(BaseFuzzyAttribute):
    """Handles fuzzy choice based on Distribution instance with weights."""

    def __init__(self, distribution: Distribution, **kwargs):
        self.distribution = distribution
        super(FuzzyDistributedChoice, self).__init__(**kwargs)

    def fuzz(self):
        return self.distribution.flip()

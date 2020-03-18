from factory.random import reseed_random
from .generator import generate

if __name__ == '__main__':
    reseed_random(123)
    generate()


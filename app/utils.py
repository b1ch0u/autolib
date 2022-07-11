import string
import random as rd


def get_random_printable_str(length: int = 32) -> str:
    return ''.join(rd.choice(string.printable) for _ in range(32))


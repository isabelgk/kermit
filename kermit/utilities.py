import math
from decimal import Decimal


def near_round(x, base):
    """ Returns n rounded to the nearest multiple of m """
    return int(base * round(Decimal(x)/base))


def round_up(x, base):
    """ Returns n rounded up to the nearest multiple of m """
    return int(math.ceil(x / base) * base)


def round_down(x, base):
    """ Returns n rounded down to the nearest multiple of m """
    return int(math.floor(x / base) * base)

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


def stringify_dict(d):
    """
    Used to send calculated values to Jinja2 templates.

    Given a dictionary where all values are some kind of number,
    turn those values into strings. If the value is an integer, keep
    it as such and have no decimal places. If the value is a decimal
    or a float (although we are avoiding floats), round to two
    decimal places.

    Args:
        - d (dict):

    Returns:
        - stringified dictionary
    """
    stringified = dict()
    for key, value in d.items():
        if isinstance(value, int):
            stringified[key] = str(value)
        elif isinstance(value, Decimal):
            stringified[key] = str(value.quantize('.01'))
        elif isinstance(value, float):
            stringified[key] = str(round(value, 2))

    return stringified


def decrease_instructions(sts_in_decrease_group, closure_initial_decrease):
    s = ''
    if closure_initial_decrease != 0:
        s += '*Initial decrease round*: [k' + str(sts_in_decrease_group - 1) + ', k2tog] '\
                + str(closure_initial_decrease)  + ' times. Knit to end of the round.\n\n'
    s += 'Divide the stitches into ' + str(sts_in_decrease_group) + ' groups.\n\n'
    s += '*Decrease round*: [knit to 2 sts before end of group, k2tog] 5 times around. '
    s += 'Repeat until 5 sts remain.\n\n'
    return s

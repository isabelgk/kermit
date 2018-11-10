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


def make_str_dict(keys_list, original):
    result = dict()
    for key in keys_list:
        result[key] = str(original[key])
    return result


def sock_calculate(inputs):
    """ Given all of the form inputs, make the calculations needed. """

    calc = inputs.copy()

    calc['sock_sts'] = near_round(inputs['spi'] * inputs['foot_circ'] * Decimal(.95), 4)
    calc['heel_sts'] = calc['sock_sts'] // 2
    calc['heel_rows'] = round_up(calc['foot_circ'] * calc['row_gauge'] * Decimal(0.3), 2)
    calc['gusset_st_per_side'] = int((calc['heel_rows'] / 2) + 2)

    if calc['heel_sts'] % 3 == 2 or calc['heel_sts'] % 3 == 1:
        calc['HT1'] = (calc['heel_sts'] // 3) * 2 + 1
    else:
        calc['HT1'] = calc['heel_sts'] * 2 // 3
    if calc['heel_sts'] % 3 == 2:
        calc['HT2'] = calc['heel_sts'] // 3
    elif calc['heel_sts'] % 3 == 1:
        calc['HT2'] = int(math.floor(calc['heel_sts']) / 3 + 1)
    else:
        calc['HT2'] = int(calc['heel_sts'] / 3)

    calc['sts_after_pickup'] = int(
        (calc['sock_sts'] / 2) + (calc['HT2'] + 2) + (2 * calc['gusset_st_per_side']))
    calc['TD1'] = round_up(((calc['sock_sts'] - 8) / 8), 1)
    calc['TD2'] = round_down(((calc['sock_sts'] - 8) / 8), 1)
    calc['first_toe_dec_count'] = calc['sock_sts'] - 4 * calc['TD1']
    calc['leg_rows'] = int(
        calc['leg_length'] * calc['row_gauge'] - 20 - calc['heel_rows'])

    keys_list = ['spi', 'row_gauge', 'foot_circ', 'ankle_circ', 'gusset_circ',
                 'foot_length', 'low_calf_circ', 'heel_diag', 'leg_length', 'sock_sts',
                 'heel_sts', 'heel_rows', 'gusset_st_per_side', 'HT1', 'HT2',
                 'sts_after_pickup', 'leg_rows', 'first_toe_dec_count', 'TD1', 'TD2']

    result = make_str_dict(keys_list, calc)

    return result

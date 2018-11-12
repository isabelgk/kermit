import math
from decimal import Decimal


# UTILITIES

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


def decrease_instructions(sts_in_decrease_group, closure_initial_decrease):
    s = ''
    if closure_initial_decrease != 0:
        s += '*Initial decrease round*: [k' + str(sts_in_decrease_group - 1) + ', k2tog]'\
                + str(closure_initial_decrease)  + ' times. Knit to end of the round.\n\n'
    s += 'Divide the stitches into ' + str(sts_in_decrease_group) + ' groups.\n\n'
    s += '*Decrease round*: [knit to 2 sts before end of group, k2tog] 5 times around. '
    s += 'Repeat until 5 sts remain.\n\n'
    return s

# CALCULATIONS


def sock_calculate(parameters, inputs):
    """ Given all of the form inputs, make the calculations needed. """

    calc = inputs.copy()

    calc['sock_sts'] = near_round(parameters['spi'] * inputs['foot_circ'] * Decimal(.95), 4)
    calc['heel_sts'] = calc['sock_sts'] // 2
    calc['heel_rows'] = round_up(calc['foot_circ'] * parameters['row_gauge'] * Decimal(0.3), 2)
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
        calc['leg_length'] * parameters['row_gauge'] - 20 - calc['heel_rows'])

    keys_list = ['spi', 'row_gauge', 'foot_circ', 'ankle_circ', 'gusset_circ',
                 'foot_length', 'low_calf_circ', 'heel_diag', 'leg_length', 'sock_sts',
                 'heel_sts', 'heel_rows', 'gusset_st_per_side', 'HT1', 'HT2',
                 'sts_after_pickup', 'leg_rows', 'first_toe_dec_count', 'TD1', 'TD2']
    result = make_str_dict(keys_list, calc)

    return result


def mitten_calculate(inputs):
    calc = inputs.copy()

    # values you can estimate from the hand circumference (palm circumference)
    if 'wrist_circumference' not in calc:
        calc['wrist_circumference'] = calc['palm_circumference'] * Decimal(0.8)
    if 'hand_length' not in calc:
        calc['hand_length'] = calc['palm_circumference']
    if 'thumb_gusset_length' not in calc:  # aka gusset rounds
        calc['thumb_gusset_length'] = calc['hand_length'] * Decimal(0.36)
    if 'thumb_length' not in calc:
        calc['thumb_length'] = round(calc['hand_length'] * Decimal(0.33), 2)
    if 'rnds_per_inch' not in calc:
        calc['rnds_per_inch'] = calc['spi'] * Decimal(0.75)
    if 'ease' not in calc:
        calc['ease'] = Decimal(1.0)
    if 'cuff_length' not in calc:
        calc['cuff_length'] = Decimal(2.0)

    # TODO: gusset increase instructions
    # must calculate these
    calc['cuff_sts'] = near_round(calc['wrist_circumference'] * calc['spi'], 4)
    calc['hand_sts'] = near_round(calc['palm_circumference'] * calc['ease'] * calc['spi'], 2)
    calc['cuff_to_hand_st_increase'] = calc['hand_sts'] - calc['cuff_sts']
    calc['gusset_sts'] = near_round(calc['thumb_gusset_length'] * calc['rnds_per_inch'], 1)
    calc['sts_for_closure'] = round_down(calc['hand_sts'], 5)
    calc['closure_length'] = (Decimal((calc['sts_for_closure'] - 5)) / 5) / calc['rnds_per_inch']
    calc['closure_initial_decrease'] = calc['hand_sts'] - calc['sts_for_closure']
    calc['decrease_instructions'] = decrease_instructions(calc['sts_for_closure']//5, \
                                        calc['closure_initial_decrease'])
    calc['thumb_rows'] = near_round(calc['thumb_length'] * calc['rnds_per_inch'] - 3, 1)

    keys_list = ['spi', 'row_gauge', 'cuff_sts', 'cuff_length', 'hand_length',
                 'cuff_to_hand_st_increase', 'hand_sts', 'gusset_sts',
                 'decrease_instructions', 'thumb_length', 'thumb_rows']
    result = make_str_dict(keys_list, calc)
    return result

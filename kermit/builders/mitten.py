class Mitten():
    pass


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

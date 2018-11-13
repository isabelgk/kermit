from kermit.utilities import *


class Sock:
    """ A sock pattern object """

    def __init__(self, gauge, measurements):
        """ Constructor for the Sock """
        self.gauge = self.fill_in_needed_values(gauge, gauge=True)
        self.measurements = self.fill_in_needed_values(measurements, measurements=True)
        self.numbers = smart_stringify_dictionary(self.calculate_values(self.gauge, self.measurements))
        self.flags = self.unusual_ratios(self.measurements)

    def get_measurements(self):
        return self.numbers

    @staticmethod
    def fill_in_needed_values(d, gauge=False, measurements=False):
        """
        To generate a pattern, there are only a few needed inputs because the
        others can be calculated. We allow more inputs than needed, though,
        because getting values relies less on the average sizing and helps create
        a better fit in the final product.

        This function gathers all known numbers and calculates the necessary remaining
        values.

        Args:
            - gauge (dict): A dict holding form values from the user under "Gauge"
                - Must contain spi
                - Can contain row gauge
            - measurements (dict): A dict holding form values from the user under "Measurements"
                - Must contain one of [foot circumference, ankle circumference, gusset
                circumference, foot length]
                - Can contain lower calf circumference, heel diagonal circumference, and
                sock leg length

        Returns:
            - Dictionary with all strings for keys and numbers as values.
        """
        assert not (gauge and measurements), "You can only fill in one dictionary at a time"

        if gauge:
            # Go through gauge first: row gauge to stitches per inch is roughly 4 to 3
            if 'row_gauge' not in d:
                d['row_gauge'] = Decimal(4/3 * d['spi'])

        if measurements:
            if d['foot_length'] is not None:
                if d['foot_circ'] is None:
                    d['foot_circ'] = d['foot_length'] * Decimal(1.05)
                if d['ankle_circ'] is None:
                    d['ankle_circ'] = d['foot_length'] * Decimal(1.05)
                if d['gusset_circ'] is None:
                    d['gusset_circ'] = d['foot_length'] * Decimal(1.15)

            if d['foot_circ'] is not None:
                if d['foot_length'] is None:
                    d['foot_length'] = d['foot_circ'] * Decimal(0.95)
                if d['gusset_circ'] is None:
                    d['gusset_circ'] = d['foot_circ'] * Decimal(1.10)
                if d['ankle_circ'] is None:
                    d['ankle_circ'] = d['foot_circ']

            if d['gusset_circ'] is not None:
                if d['foot_length'] is None:
                    d['foot_length'] = d['gusset_circ'] * Decimal(0.95)
                if d['foot_circ'] is None:
                    d['foot_circ'] = d['gusset_circ'] / Decimal(1.10)
                if d['ankle_circ'] is None:
                    d['ankle_circ'] = d['gusset_circ'] * Decimal(1.05)

            if d['ankle_circ'] is not None:
                if d['foot_length'] is None:
                    d['foot_length'] = d['ankle_circ'] * Decimal(0.95)
                if d['foot_circ'] is None:
                    d['foot_circ'] = d['ankle_circ']
                if d['gusset_circ'] is None:
                    d['gusset_circ'] = d['ankle_circ'] * Decimal(1.10)

            if d['leg_length'] is None:
                d['leg_length'] = Decimal(8)

        return d

    @staticmethod
    def unusual_ratios(measurements):
        """
        From the measurements, there may be some unusual ratios that will require
        extra changes to the pattern.

        Args:
            - Measurements (dict)

        Returns:
            - list of unusual ratios to set as a flag on the object
        """
        flags = []

        return flags

    @staticmethod
    def calculate_values(gauge, measurements):
        """
        Given your gauge and foot measurements, get all of the needed numbers for the sock pattern.

        Args:
            - gauge (dict): Stitches per inch and rounds per inch
            - measurements (dict): foot circumference, ankle circumference, gusset circumference, foot length,
            lower calf circumference, heel diagonal circumference, sock leg length
        """
        numbers = dict()
        numbers['sock_sts'] = near_round(gauge['spi'] * measurements['foot_circ'] * Decimal(.95), 4)
        numbers['heel_sts'] = numbers['sock_sts'] // 2
        numbers['heel_rows'] = round_up(measurements['foot_circ'] * gauge['row_gauge'] * Decimal(0.3), 2)
        numbers['gusset_st_per_side'] = int((numbers['heel_rows'] / 2) + 2)

        if numbers['heel_sts'] % 3 == 2 or numbers['heel_sts'] % 3 == 1:
            numbers['HT1'] = (numbers['heel_sts'] // 3) * 2 + 1
        else:
            numbers['HT1'] = numbers['heel_sts'] * 2 // 3
        if numbers['heel_sts'] % 3 == 2:
            numbers['HT2'] = numbers['heel_sts'] // 3
        elif numbers['heel_sts'] % 3 == 1:
            numbers['HT2'] = int(math.floor(numbers['heel_sts']) / 3 + 1)
        else:
            numbers['HT2'] = int(numbers['heel_sts'] / 3)

        numbers['sts_after_pickup'] = int(
            (numbers['sock_sts'] / 2) + (numbers['HT2'] + 2) + (2 * numbers['gusset_st_per_side']))
        numbers['TD1'] = round_up(((numbers['sock_sts'] - 8) / 8), 1)
        numbers['TD2'] = round_down(((numbers['sock_sts'] - 8) / 8), 1)
        numbers['first_toe_dec_count'] = numbers['sock_sts'] - 4 * numbers['TD1']
        numbers['leg_rows'] = int(
            measurements['leg_length'] * gauge['row_gauge'] - 20 - numbers['heel_rows'])

        return numbers


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


if __name__ == "__main__":
    import doctest
    doctest.testmod()

from decimal import Decimal
from kermit.utilities import round_down, round_up, near_round, stringify_dict


class Sock:
    """ A builders pattern object """

    def __init__(self, metadata, gauge, measurements, design):
        """ Constructor for the Sock """
        self.metadata = metadata
        self.gauge = self.fill_in_needed_values(gauge, gauge=True)
        self.measurements = self.fill_in_needed_values(measurements, measurements=True)
        self.all_data = self.calculate_values(self.gauge, self.measurements)
        self.design = design

        self.pattern = self.get_pattern_text_dict()
        print(self.pattern)

    def __str__(self):
        """ The sock's string is its pattern. """
        text = ""
        for key, value in self.pattern.items():
            text += "{}\n".format(key)
            for item in value:
                text += "{}\n".format(item)
        return text

    def get_calculated_sock_numbers(self):
        return stringify_dict(self.calculate_values(self.gauge, self.measurements))

    def get_intro_text(self):
        """
        Let the user know about the name of the pattern and the gauge.

        Note: For Jinja2, we will separate new lines by creating each line of text as an
        element in an array and will display as follows:
            {% for para in text %}
            <p>{{para}}</p>
            {% endfor %}

        This is because Jinja2 does not interpret \n or <br> correctly.
        https://stackoverflow.com/questions/12244057/any-way-to-add-a-new-line-from-a-string-with-the-n-character-in-flask
        """
        text = []
        if self.metadata['name'] is not None:
            text.append("{}".format(self.metadata['name']))
        text.append("stitches per inch: {}".format(self.gauge['spi']))
        text.append("rounds per inch: {}".format(self.gauge['row_gauge']))

        return text

    def get_cuff_text(self):
        """
        Return the text of the cuff as a list.

        There are currently two kinds of ribbing we can use on the cuff:
            - 1x1 rib
            - 2x2 rib
        """

        if self.design['cuff_ribbing'] == 'one_by_one':
            rib = "1x1 ribbing"
        elif self.design['cuff_ribbing'] == 'two_by_two':
            rib = "2x2 ribbing"
        else:
            rib = "ribbing"

        text = [
            "Cast on {} stitches and join in the round.".format(self.all_data['sock_sts']),
            "Work in {} for 2 inches.".format(rib)
        ]

        return text

    def get_leg_text(self):
        """
        Return the text for working the leg in a list.

        This is generic and uses "pattern stitch" to describe how to work the leg but this
        could be updated later.
        """
        text = ["Continue even in pattern stitch for {} rows.".format(self.all_data['leg_rows'])]

        return text

    def get_heel_flap_text(self):
        """
        Return the text for making the heel flap in a list.

        Three types of heel flap are currently supported:
            - Stockinette ('stockinette')
            - Slip stitch ('slip_stitch')
            - Eye of Partridge ('eye_of_partridge')
        """
        text = []
        text.append("Slip {} stitches onto a needle so you can work the heel flap. You "
                    "will be working in rows for this section.".format(self.all_data['heel_sts']))

        if self.design['heel_stitch_pattern'] == "stockinette":
            lst = [
                "    1. (RS) Knit {} stitches, ssk, turn work.".format(self.all_data['heel_sts']),
                "    2. (WS) Slip 1 purlwise wyif, purl to end of heel stitches, turn work.",
                "    3. (RS) Slip 1 purlwise wyib, knit to end of heel stitches, turn work.",
                "    4. (WS) Slip 1 purlwise wyif, purl to end of heel stitches, turn work.",
                "Repeat rows 3 and 4 until {} rows have been worked in total.".format(self.all_data['heel_rows'])
            ]
            text.extend(lst)

        elif self.design['heel_stitch_pattern'] == "slip_stitch":
            if self.all_data['heel_sts'] % 2 == 0:
                text.append("    1. (RS) *Slip 1 purlwise wyib, knit 1; repeat from *.")
            else:
                text.append("    1. (RS) *Slip 1 purlwise wyib, knit 1; repeat from * to last stitch. Knit 1.")

            text.append("    2. (WS) Slip 1 purlwise wyif, purl to end.")
            text.append("Repeat rows 1 and 2 until {} rows "
                        "have been worked in total.".format(self.all_data['heel_rows']))

        elif self.design['heel_stitch_pattern'] == "eye_of_partridge":
            if self.all_data['heel_sts'] % 2 == 0:
                lst = [
                    "    1. (RS) *Slip 1 purlwise wyib, knit 1; repeat from *.",
                    "    2. (WS) Purl all stitches.",
                    "    3. (RS) Slip 1 purlwise wyib, *slip 1 purlwise wyib, knit 1; repeat from * to last stitch."
                    "Knit 1.",
                    "    4. (WS) Purl all stitches."
                ]
            else:
                lst = [
                    "    1. (RS) *Slip 1 purlwise wyib, knit 1; repeat from * to last stitch. Knit 1.",
                    "    2. (WS) Purl all stitches.",
                    "    3. (RS) Slip 1 purlwise wyib, *slip 1 purlwise wyib, knit 1; repeat from *.",
                    "    4. (WS) Purl all stitches."
                ]
            text.extend(lst)
            text.append("Repeat rows 1-4 until {} rows have been worked in total.".format(self.all_data['heel_rows']))

        else:
            text.append("Something went wrong. Use your heel flap pattern here.")

        return text

    def get_heel_turn_text(self):
        """
        Return in a list the text for making the heel flap.

        See here for diagrams: https://tutorials.knitpicks.com/heels-and-toes-glossary/
        See here for general instructions: http://www.socknitters.com/Tips/heels_by_the_number.htm

        There are four heel turn types supported:
            - Dutch ('square_heel')
            - French ('round_heel')
            - Handkerchief ('v_heel')
            - German Strap ('band_heel')
        """
        text = []

        if self.design['heel_turn'] == 'square_heel':
            set_up = self.all_data['heel_sts'] * 2 // 3
            remaining = self.all_data['heel_sts'] - set_up
            text.append('You are working the square heel.')
            text.append('    1. (RS) Knit {} stitches, ssk, turn work.'.format(set_up))
            text.append('    2. (WS) Slip 1 purlwise wyif, purl {} stitches, p2tog, turn work.'.format(remaining))
            text.append('    3. (RS) Slip 1 purlwise wyib, knit {} stitches, ssk, turn work.'.format(remaining))
            text.append('    4. (WS) Slip 1 purlwise wyif, purl {} stitches, p2tog, turn work'.format(remaining))
            text.append('Repeat rows 3 and 4 until all heel stitches have been worked, ending after a WS row.')

        elif self.design['heel_turn'] == 'round_heel':
            set_up = round_up(self.all_data['heel_sts'] // 2, 1) + 1
            text.append('You are working the round heel.')
            text.append('    1. (RS) Slip 1 purlwise wyib, knit {} stitches, ssk, knit 1, turn work.'
                        .format(set_up)
                        )
            text.append('    2. (WS) Slip 1 purlwise wyif, purl 5 stitches, p2tog, purl 1, turn work.')
            text.append('    3. (RS) Slip 1 purlwise wyib, knit 6 stitches, ssk, knit 1, turn work.')
            text.append('    4. (WS) Slip 1 purlwise wyif, purl 7 stitches, p2tog, purl 1, turn work.')
            text.append('Continue working one more stitch until all have been worked.')

        elif self.design['heel_turn'] == 'v_heel':
            set_up = self.all_data['heel_sts'] // 2 - 1
            text.append('You are working the V-heel.')
            text.append('    1. (RS) Slip 1 purlwise wyib, knit {} stitches - 1, ssk, knit 1, turn work.'
                        .format(set_up)
                        )
            text.append('    2. (WS) Slip 1 purlwise wyif, purl 1 stitch, p2tog, purl 1, turn work.')
            text.append('    3. (RS) Slip 1 purlwise wyib, knit 2 stitches, ssk, knit 1, turn work.')
            text.append('    4. (WS) Slip 1 purlwise wyif, purl 3 stitches, p2tog, purl 1, turn work.')
            text.append('Continue working one more stitch until all have been worked.')

        elif self.design['heel_turn'] == 'band_heel':
            set_up = self.all_data['heel_sts'] * 3 // 4
            remaining = self.all_data['heel_sts'] // 2
            text.append('You are working the band heel.')
            text.append('    1. (RS) Slip 1 purlwise wyib, knit {} stitches, k2tog, turn work.'.format(set_up))
            text.append('    2. (WS) Slip 1 purlwise wyif, purl {} stitches, p2tog, turn work.'.format(remaining))
            text.append('    3. (RS) Slip 1 purlwise wyib, knit {} stitches, k2tog, turn work.'.format(remaining))
            text.append('    4. (WS) Slip 1 purlwise wyif, purl {} stitches, p2tog, turn work.'.format(remaining))
            text.append('Continue working the last two rows until all stitches have been worked.')

        else:
            text.append("Something went wrong. Use your heel turn pattern here.")

        return text

    def get_gusset_text(self):
        """
        Return in a list the text for working the gusset.

        Needs to calculate the gusset stitches per side and the number of stitches after pick up.
        """
        gusset_st_per_side = self.all_data['heel_rows'] // 2 + 2
        total_sts = self.all_data['sock_sts'] + gusset_st_per_side

        text = [
            'Begin the stitch pick ups. Keep the RS facing you and pick up {} stitches along the first '
            'side of your heel flap. Make sure to pick up the last two stitches above the break between '
            'the heel and instep stitches.'.format(gusset_st_per_side),

            'Work across the instep stitches in your desired stitch pattern.',

            'Again with RS facing you, pick up and knit {} stitches on the other side of the heel flap. '
            'Make sure you pick up the last two stitches above the break as before.'.format(gusset_st_per_side),

            'You should have {} stitches on the needles.'.format(total_sts)
        ]

        return text

    def get_foot_text(self):
        """
        Return in a list the text for working the foot.

        The only logic in this section is that fewer cast on stitches require starting later for toe decreases.
        """
        if self.all_data['sock_sts'] <= 50:
            length = self.measurements['foot_length'] - Decimal(1.5)
        else:
            length = self.measurements['foot_length'] - Decimal(2)

        text = ["Work even until piece is {} inches long.".format(length.quantize(Decimal('.1')))]

        return text

    def get_toe_text(self):
        """
        Return in a list the text for working the toe.

        There are two toe types supported:
            - half-and-half ("half_and_half")
            - simple ("simple")
        """

        text = []
        decrease_text = "* Decrease round: Knit to 3 stitches before instep, k2tog, knit 2, ssk, knit to " \
                        "3 stitches before end of instep, k2tog, knit 2, ssk, knit to end of round.  " \
                        "(4 stitches decreased)"
        plain_text = "* Knit even round: Knit all stitches."

        if self.design['toe_shaping'] == 'half_and_half':
            sts_to_decrease = round_up(self.all_data['sock_sts'] - round_down(self.gauge['spi'], 2), 4)
            remaining_sts = self.all_data['sock_sts'] - sts_to_decrease
            decrease_rounds = sts_to_decrease // 4
            spaced_decrease_rounds = round_up(decrease_rounds / 2, 1)
            continuing_decrease_rounds = decrease_rounds - spaced_decrease_rounds
            text.append(decrease_text)
            text.append(plain_text)
            text.append("Complete a decrease round and a knit even round grouping {} times (total: {} rounds)".
                        format(decrease_rounds, decrease_rounds*2))
            text.append("Complete a decrease round {} times (total: {} rounds)".format(continuing_decrease_rounds,
                                                                                       continuing_decrease_rounds))
            text.append("You should have {} stitches remaining. Cut the yarn, leaving a tail,"
                        "and use a tapestry needle to pull yarn through the remaining stitches. Weave in ends and "
                        "block as desired.".format(remaining_sts))

        elif self.design['toe_shaping'] == 'simple':
            sts_to_decrease = round_down(self.all_data['sock_sts'] // 3, 4)
            remaining_sts = self.all_data['sock_sts'] - sts_to_decrease
            decrease_rounds = sts_to_decrease // 4
            text.append(decrease_text)
            text.append(plain_text)
            text.append("Complete a decrease round and a knit even round grouping {} times (total: {} rounds)".
                        format(decrease_rounds, decrease_rounds * 2))
            text.append("You should have {} stitches remaining. Cut your yarn and graft the toe with Kitchener"
                        "stitch. Block as desired.".format(remaining_sts))

        else:
            text.append("Something went wrong. Your toe decrease text goes here.")

        return text

    def get_pattern_text_dict(self):
        return {'intro': self.get_intro_text(),
                'cuff': self.get_cuff_text(),
                'leg': self.get_leg_text(),
                'heel_flap': self.get_heel_flap_text(),
                'heel_turn': self.get_heel_turn_text(),
                'gusset': self.get_gusset_text(),
                'foot': self.get_foot_text(),
                'toe': self.get_toe_text()}

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
                builders leg length

        Returns:
            - Dictionary with all strings for keys and numbers as values.
        """
        assert not (gauge and measurements), "You can only fill in one dictionary at a time"

        if gauge:
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
                d['leg_length'] = Decimal(8.00)

        return d

    @staticmethod
    def unusual_ratios(measurements):
        # TODO: Unusual ratio determination
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
        Given your gauge and foot measurements, get all of the needed numbers for the builders pattern.

        Args:
            - gauge (dict): Stitches per inch and rounds per inch
            - measurements (dict): foot circumference, ankle circumference, gusset circumference, foot length,
            lower calf circumference, heel diagonal circumference, builders leg length
        """
        numbers = dict()
        numbers['sock_sts'] = near_round(gauge['spi'] * measurements['foot_circ'] * Decimal(.95), 4)
        numbers['heel_sts'] = numbers['sock_sts'] // 2
        numbers['heel_rows'] = round_up(measurements['foot_circ'] * gauge['row_gauge'] * Decimal(0.3), 2)
        numbers['gusset_st_per_side'] = int((numbers['heel_rows'] / 2) + 2)

        # This section will be deprecated and moved to the get_heel_turn_text.
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

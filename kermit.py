import math
import os
import argparse

from kermit import app
from string import Template
from weasyprint import HTML
from markdown2 import markdown_path


# UTILITIES

def near_round(x, base):
    """ Returns n rounded to the nearest multiple of m """
    return int(base * round(float(x)/base))

def round_up(x, base):
    """ Returns n rounded up to the nearest multiple of m """
    return int(math.ceil(x / base) * base)

def round_down(x, base):
    """ Returns n rounded down to the nearest multiple of m """
    return int(math.floor(x / base) * base)


def save_to_file(pattern_text, filename):
    """ Write the pattern to a new file. """
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    with open(BASE_DIR + '/created_patterns/'+ filename + '.md', 'w') as f:
        f.write(pattern_text)

def make_pdf(filename):
    """ Given a markdown file, convert to a PDF. """
    html = markdown_path('created_patterns/' + filename + '.md')
    output = 'created_patterns/' + '.'.join([filename.rsplit('.', 1)[0], 'pdf'])
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    css_file = os.path.join(BASE_DIR, 'resources/style.css')
    HTML(string=html).write_pdf(output, stylesheets=[css_file])


# PATTERN OBJECTS

class TopDownSock:
    def __init__(self, inputs, filename=None):
        """
        A sock needs certain variables to be specified to generate
        a pattern. This initializes a dictionary of the necessary quantities
        and their values. All values are assumed to be in inches.

        - spi (stitches per inch of the gauge)
        - row_gauge (stitches per inch for rows)
        - foot_circ (circumference of the ball of the foot)
        - ankle_circ (circumference of the leg around the ankle)
        - gusset_circ (circumference of the largest section of the foot)
        - foot_length (length of the foot from toe to heel)
        - low_calf_circ (circumference of leg where the top of sock will be)
        - heel_diag (circumference around the heel)
        - leg_length (length of the sock leg)
            
        >>> example = {
        ...    'spi': 8,
        ...    'row_gauge': 6,
        ...    'foot_circ': 9,
        ...    'ankle_circ': 9,
        ...    'gusset_circ': 9.78,
        ...    'foot_length': 9.5,
        ...    'low_calf_circ': 10.1,
        ...    'heel_diag': 12.2,
        ...    'leg_length': 12
        ...    }
        >>> test = TopDownSock(example, filename="example")
        """
        self.inputs = inputs
        self.calc = self.calc_pattern_values(self.inputs)


    def __str__(self):
        vals = self.calc_pattern_values(self.inputs)
        s = ""
        for number, value in vals.items():
            s += number + ": " + str(value) + "\n"
        return s


    def calc_pattern_values(self, inputs):
        """
        Return a dictionary containing all of the values calculated plus the ones
        provided.
        """
        calc = inputs.copy()

        calc['sock_sts'] = near_round(calc['spi'] * calc['foot_circ'] * .95, 4)
        calc['heel_sts'] = calc['sock_sts'] // 2
        calc['heel_rows'] = round_up(calc['foot_circ'] * calc['row_gauge'] * 0.3, 2)
        calc['gusset_st_per_side'] = int((calc['heel_rows'] / 2) + 2)

        if calc['heel_sts'] % 3 == 2 or calc['heel_sts'] % 3 == 1:
            calc['HT1'] = (calc['heel_sts'] // 3) * 2 + 1
        else:
            calc['HTI'] = calc['heel_sts'] * 2 // 3

        if calc['heel_sts'] % 3 == 2:
            calc['HT2'] = calc['heel_sts'] // 3
        elif calc['heel_sts'] % 3 == 1:
            calc['HT2'] = int(math.floor(calc['heel_sts'])/3 + 1)
        else:
            calc['HT2'] = int(calc['heel_sts'] / 3)

        calc['sts_after_pickup'] = int(
            (calc['sock_sts'] / 2) + (calc['HT2'] + 2) + (2 * calc['gusset_st_per_side']))
        calc['TD1'] = round_up(((calc['sock_sts'] - 8) / 8), 1)
        calc['TD2'] = round_down(((calc['sock_sts'] - 8) / 8), 1)
        calc['first_toe_dec_count'] = calc['sock_sts'] - 4 * calc['TD1']
        calc['leg_rows'] = int(
            calc['leg_length']*calc['row_gauge'] - 20 - calc['heel_rows'])
        return calc


    def make_pattern(self, replace_dict):
        with open('raw/socks/top_down_socks.txt', 'r') as f:
            pattern_template = f.read()
        return Template(pattern_template).safe_substitute(replace_dict)


class Mitten:
    """ A basic mitten pattern. """
    def __init__(self, inputs, filename=None):
        self.calc = self.calc_pattern_values(inputs)
        self.pattern = self.make_pattern(self.calc)
        if filename:
            save_to_file(self.pattern, filename)
            make_pdf(filename)


    def __str__(self):
        vals = self.pattern_values
        s = ""
        for number, value in vals.items():
            s += number + ": " + str(value) + "\n"
        return s


    def make_decrease_rnd(self, start, end):
        sts_to_decrease = start - end
        num_times = sts_to_decrease
        knit_group = start // sts_to_decrease - 2
        s = "[k" + str(knit_group) + ", k2tog] " + str(num_times) + " times"
        decrease_group_leftover = start % sts_to_decrease
        if decrease_group_leftover != 0:
            s += ", k" + str(decrease_group_leftover) + " to end of round"
        return s


    def decrease_instructions(self, sts_in_decrease_group, closure_initial_decrease):
        s = ''
        if closure_initial_decrease != 0:
            s += '*Initial decrease round*: [k' + str(sts_in_decrease_group - 1) + ', k2tog]'\
                    + str(closure_initial_decrease)  + ' times. Knit to end of the round.\n\n'
        s += 'Divide the stitches into ' + str(sts_in_decrease_group) + ' groups.\n\n'
        s += '*Decrease round*: [knit to 2 sts before end of group, k2tog] 5 times around. '
        s += 'Repeat until 5 sts remain.\n\n'

        return s


    def make_pattern(self, replace_dict):
        with open('raw/mittens/basic_mitten.txt', 'r') as f:
            pattern_template = f.read()
        return Template(pattern_template).safe_substitute(replace_dict)



    def calc_pattern_values(self, inputs):
        calc = inputs.copy()

        # values you can estimate from the hand circumference (palm circumference)
        if 'wrist_circumference' not in calc:
            calc['wrist_circumference'] = calc['palm_circumference'] * 0.8
        if 'hand_length' not in calc:
            calc['hand_length'] = calc['palm_circumference']
        if 'thumb_gusset_length' not in calc:  # aka gusset rnds
            calc['thumb_gusset_length'] = calc['hand_length'] * 0.36
        if 'thumb_length' not in calc:
            calc['thumb_length'] = calc['hand_length'] * 0.33
        if 'ease' not in calc:
            calc['ease'] = 1
        if 'rnds_per_inch' not in calc:
            calc['rnds_per_inch'] = calc['gauge'] * 0.75

        # must calculate these
        calc['cuff_sts'] = near_round(calc['wrist_circumference'] * calc['gauge'], 4)
        calc['hand_sts'] = near_round(calc['palm_circumference'] * calc['ease'] * calc['gauge'], 2)
        calc['cuff_to_hand_st_increase'] = calc['hand_sts'] - calc['cuff_sts']
        calc['gusset_sts'] = near_round(calc['thumb_gusset_length'] * calc['rnds_per_inch'], 1)
        calc['sts_for_closure'] = round_down(calc['hand_sts'], 5)
        calc['closure_length'] = ((calc['sts_for_closure'] - 5) / 5) / calc['rnds_per_inch']
        calc['closure_initial_decrease'] = calc['hand_sts'] - calc['sts_for_closure']
        calc['decrease_instructions'] = self.decrease_instructions(calc['sts_for_closure']//5, \
                                            calc['closure_initial_decrease'])
        calc['thumb_rows'] = near_round(calc['thumb_length'] * calc['rnds_per_inch'] - 3, 1)

        return calc


if __name__ == "__main__":
    test = {"palm_circumference": 8, "gauge": 8}
    example = Mitten(test, 'test')

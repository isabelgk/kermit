import math
import os
import argparse

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
        self.numbers = self.calc_pattern_values(self.inputs)
        self.pattern = self.make_pattern(self.numbers)
        if filename:
            save_to_file(self.pattern, filename)
            make_pdf(filename)


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
        numbers = inputs.copy()

        numbers['sock_sts'] = near_round(numbers['spi'] * numbers['foot_circ'] * .95, 4)
        numbers['heel_sts'] = numbers['sock_sts'] // 2
        numbers['heel_rows'] = round_up(numbers['foot_circ'] * numbers['row_gauge'] * 0.3, 2)
        numbers['gusset_st_per_side'] = int((numbers['heel_rows'] / 2) + 2)

        if numbers['heel_sts'] % 3 == 2 or numbers['heel_sts'] % 3 == 1:
            numbers['HT1'] = (numbers['heel_sts'] // 3) * 2 + 1
        else:
            numbers['HTI'] = numbers['heel_sts'] * 2 // 3

        if numbers['heel_sts'] % 3 == 2:
            numbers['HT2'] = numbers['heel_sts'] // 3
        elif numbers['heel_sts'] % 3 == 1:
            numbers['HT2'] = int(math.floor(numbers['heel_sts'])/3 + 1)
        else:
            numbers['HT2'] = int(numbers['heel_sts'] / 3)

        numbers['sts_after_pickup'] = int(
            (numbers['sock_sts'] / 2) + (numbers['HT2'] + 2) + (2 * numbers['gusset_st_per_side']))
        numbers['TD1'] = round_up(((numbers['sock_sts'] - 8) / 8), 1)
        numbers['TD2'] = round_down(((numbers['sock_sts'] - 8) / 8), 1)
        numbers['first_toe_dec_count'] = numbers['sock_sts'] - 4 * numbers['TD1']
        numbers['leg_rows'] = int(
            numbers['leg_length']*numbers['row_gauge'] - 20 - numbers['heel_rows'])
        return numbers


    def make_pattern(self, replace_dict):
        with open('template_patterns/top_down_socks.txt', 'r') as f:
            pattern_template = f.read()
        return Template(pattern_template).safe_substitute(replace_dict)


class Mitten:
    """ A basic mitten pattern. """
    def __init__(self, measurements=None, filename=None):
        """
        The mitten needs some variables to calculate the pattern.
        - spi
        - row_gauge
        - cuff_sts
        - cuff_length
        - cuff_to_hand_st_increase
        - hand_sts
        - gusset_sts
        - gusset_rnds
        - closure_sts
        - closure_length
        - closure_init_dec
        - sts_in_dec_group
        - ease
        """
        if inputs == None and 
            if hand_circumference != None:
                inputs = self.estimate_measurements(hand_circumference)
            else:
                inputs = self.estimate_measurements()
        self.inputs = inputs

    def estimate_measurements(self, hand_circumference=7):
        """
        If you do not know anything except a hand circumference, 
        you can estimate measurements from there.
        """
        estimate = dict()
        hand_length = hand_circumference
        estimate[cuff_sts] = near_round(0.8 * hand_circumference, 4)
        estimate[cuff_length] = 


    def hand_to_upper_ribbing_decrease_instructions(self):
        """ """
        pass


    def calc_pattern_values(self, inputs):
        """ """
        numbers = self.inputs.copy()


    def make_pattern(self, replace_dict):
        """ """
        pass


# if __name__ == "__main__":
    # pass

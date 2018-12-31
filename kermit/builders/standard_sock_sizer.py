import yaml


def sock_sizer(d):
    """
    Uses standard shoe sizes to estimate the dimensions for a sock.

    Args:
        - (dict) dictionary: contains three key value pairs
            1. 'foot_sizing_standard': one of 'us', 'eu', or 'uk'
            2. 'style': one of 'men', 'women', 'child', or 'kid'
            3. 'size': a float for the shoe size

    Returns:
        - (dict) containing:
            - 'foot_circumference': (float)
            - 'foot_length': (float)
    """
    with open('kermit/static/sock/standard-sizes.yml', 'r') as f:
        table = yaml.load(f)

    return {'foot_circ': table[d['style']][d['foot_sizing_standard']][d['size']][0],
            'foot_length': table[d['style']][d['foot_sizing_standard']][d['size']][1],
            'ankle_circ': None,
            'gusset_circ': None,
            'low_calf_circ': None,
            'heel_diag': None,
            'leg_length': None,
            }

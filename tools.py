""" This script define tools function used by the GUI """
import re


def check_page_nums(page_range):
    """ Check all page ranges from the gui """
    page_num_list = re.split(',', page_range)
    pattern = re.compile("^([0-9]*)(\-[0-9]*)?[o|e]?$")
    return all(pattern.match(page_num) for page_num in page_num_list)


def is_acceptable_number(number, type, minval, maxval):
    """ Check if a number is float or int """
    if type == 'int':
        if isinstance(number, int) and number >= minval and number <= maxval:
            return True
    elif type == 'float':
        if isinstance(number, int):
            return False
        try:
            number = float(number)
        except ValueError:
            return False
        if number >= minval and number <= maxval:
            return True

    return False
# tools_function
import re

def check_page_nums(input_pages):
    page_num_list = re.split(',|-|o|e', input_pages)
    return all((page_num and page_num.isdigit() for page_num in page_num_list))

def is_acceptable_number(number, type, minval, maxval):
    ''' Check if a number is float or int '''
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

# tools_function

def check_page_nums(input_pages):
    page_num_list = re.split(',|-|o|e', input_pages)

    for page_num in page_num_list:
        if len(page_num) > 0 and not page_num.isdigit():
            return False
    return True

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
# tools_function

def check_page_nums(input_pages):
    page_num_list = re.split(',|-|o|e', input_pages)

    for page_num in page_num_list:
        if len(page_num) > 0 and not page_num.isdigit():
            return False
    return True
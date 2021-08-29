# Test
from tools import check_page_nums, is_acceptable_number

def test_is_acceptable_number():
    a = 3
    assert is_acceptable_number(a, 'int', 0, 5) == True
    assert is_acceptable_number(a, 'int', 0, 3.141592) == True
    assert is_acceptable_number(a, 'int', 0, 2) == False
    assert is_acceptable_number(a, 'int', 4, 5) == False
    assert is_acceptable_number(a, 'float', 0, 5) == False
    a = 3.141592
    assert is_acceptable_number(a, 'float', 0, 5) == True
    assert is_acceptable_number(a, 'float', 0, 3.141592) == True
    assert is_acceptable_number(a, 'float', 0, 2) == False
    assert is_acceptable_number(a, 'float', 4, 5) == False
    assert is_acceptable_number(a, 'int', 0, 5) == False
    a = '0.200'
    assert is_acceptable_number(a, 'float', 0, 5) == True
    assert is_acceptable_number(a, 'float', 0, 5) == True
    assert is_acceptable_number(a, 'float', 0, 3.141592) == True
    assert is_acceptable_number(a, 'float', 0, 2) == True
    assert is_acceptable_number(a, 'float', 4, 5) == False
    assert is_acceptable_number(a, 'int', 0, 5) == False

def test_check_page_nums():
    page_range = '5-51o'        # Page range find on the k2pdfopt official website
    assert check_page_nums(page_range) == True
    page_range = '1,2-5,13,15'  # Page range find on the k2pdfopt official website
    assert check_page_nums(page_range) == True
    page_range = '1,3,5-10'     # Page range find on the k2pdfopt official website
    assert check_page_nums(page_range) == True
    page_range = '1-3,5,9,10-'  # Page range find on the k2pdfopt official website
    assert check_page_nums(page_range) == True
    page_range = '2-52e,3-33o'  # Page range find on the k2pdfopt official website
    assert check_page_nums(page_range) == True
    page_range = 'o,e'          # Page range find on the k2pdfopt official website
    assert check_page_nums(page_range) == True
    page_range = '2-5e,3-7o,9-'
    assert check_page_nums(page_range) == True
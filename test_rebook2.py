# Test
from rebook2 import ReBook, MainFrame
k2pdfopt_path = './k2pdfopt'

def test_generate_command_with_empty_default_var_map():
    rebook = ReBook()
    frame = MainFrame(rebook, k2pdfopt_path)
    frame.k2pdfopt_cmd_args = {}
    assert frame.generate_command_argument_string() == '-a- -ui- -x'

def test_generate_command_with_default_var_map():
    rebook = ReBook()
    frame = MainFrame(rebook, k2pdfopt_path)
    assert frame.generate_command_argument_string() == '-mode def -rt 0 -ws 0.200 -wrap+ -dev k2 -a- -ui- -x'
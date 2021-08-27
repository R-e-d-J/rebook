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

def test_generate_command_for_mode():
    rebook = ReBook()
    frame = MainFrame(rebook, k2pdfopt_path)
    for mode_argument in MainFrame.mode_argument_map:
        frame.k2pdfopt_cmd_args = {}
        frame.k2pdfopt_cmd_args[frame.conversion_mode_arg_name] = frame.conversion_mode_arg_name + ' ' + MainFrame.mode_argument_map[mode_argument]
        assert frame.generate_command_argument_string() == frame.conversion_mode_arg_name + ' ' + MainFrame.mode_argument_map[mode_argument] + ' -a- -ui- -x'

def test_generate_commande_for_device():
    rebook = ReBook()
    frame = MainFrame(rebook, k2pdfopt_path)
    for device in MainFrame.device_argument_map:
        if MainFrame.device_argument_map[device] is not None:
            frame.k2pdfopt_cmd_args = {}
            frame.k2pdfopt_cmd_args[frame.device_arg_name] = frame.device_arg_name + ' ' + MainFrame.device_argument_map[device]
            assert frame.generate_command_argument_string() == frame.device_arg_name + ' ' + MainFrame.device_argument_map[device] + ' -a- -ui- -x'
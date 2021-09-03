# Test
import rebook2
k2pdfopt_path = './k2pdfopt'

def test_generate_command_with_empty_default_var_map():
    rebook = rebook2.ReBook()
    frame = rebook2.MainFrame(rebook, k2pdfopt_path)
    frame.k2pdfopt_command_args = {}
    assert frame.generate_command_argument_string() == '-a- -ui- -x'

def test_generate_command_with_default_var_map():
    rebook = rebook2.ReBook()
    frame = rebook2.MainFrame(rebook, k2pdfopt_path)
    assert frame.generate_command_argument_string() == '-mode def -ehl 1 -evl 1 -rt 0 -ws 0.200 -sm -wrap+ -dev k2 -a- -ui- -x'

def test_generate_command_for_mode():
    rebook = rebook2.ReBook()
    frame = rebook2.MainFrame(rebook, k2pdfopt_path)
    for mode_argument in rebook2.MODE_ARGUMENT_MAP:
        frame.k2pdfopt_command_args = {}
        frame.k2pdfopt_command_args[rebook2.CONVERSION_MODE_ARG_NAME] = rebook2.CONVERSION_MODE_ARG_NAME + ' ' + rebook2.MODE_ARGUMENT_MAP[mode_argument]
        assert frame.generate_command_argument_string() == rebook2.CONVERSION_MODE_ARG_NAME + ' ' + rebook2.MODE_ARGUMENT_MAP[mode_argument] + ' -a- -ui- -x'

def test_generate_commande_for_device():
    rebook = rebook2.ReBook()
    frame = rebook2.MainFrame(rebook, k2pdfopt_path)
    for device in rebook2.DEVICE_ARGUMENT_MAP:
        if rebook2.DEVICE_ARGUMENT_MAP[device] is not None:
            frame.k2pdfopt_command_args = {}
            frame.k2pdfopt_command_args[rebook2.DEVICE_ARG_NAME] = rebook2.DEVICE_ARG_NAME + ' ' + rebook2.DEVICE_ARGUMENT_MAP[device]
            assert frame.generate_command_argument_string() == rebook2.DEVICE_ARG_NAME + ' ' + rebook2.DEVICE_ARGUMENT_MAP[device] + ' -a- -ui- -x'

def test_generate_commande_device_correspondance():
    ''' Check if for each element of MainFrame.device_choice_map there is an correspondence in
        MainFrame.device_argument_map whitch allow to build a correct command.
    '''
    rebook = rebook2.ReBook()
    frame = rebook2.MainFrame(rebook, k2pdfopt_path)
    for device in rebook2.DEVICE_CHOICE_MAP:
        if rebook2.DEVICE_CHOICE_MAP[device] != 'Other (specify width & height)':
            frame.k2pdfopt_command_args = {}
            frame.k2pdfopt_command_args[rebook2.DEVICE_ARG_NAME] = rebook2.DEVICE_ARG_NAME + ' ' + rebook2.DEVICE_ARGUMENT_MAP[device]
            assert frame.generate_command_argument_string() == rebook2.DEVICE_ARG_NAME + ' ' + rebook2.DEVICE_ARGUMENT_MAP[device] + ' -a- -ui- -x'

# def test_cleaning_command_line_from_cbox():
#     '''
#     '''
#     rebook = ReBook()
#     frame = MainFrame(rebook, k2pdfopt_path)
#     result = '-mode def -rt 0 -ws 0.200 -wrap+ -ehl 1 -evl 1 -sm -dev kp3 -a- -ui- -x'
#     frame.strvar_command_args = '-mode def -rt 0 -ws 0.200 -wrap+ -cbox5-51o 0.5,1.0,7.0,5.2 -ehl 1 -evl 1 -sm -dev kp3 -a- -ui- -x'
#     frame.cleaning_command_line_from_cbox()
#     assert frame.strvar_command_args == result
#     frame.strvar_command_args = '-mode def -rt 0 -ws 0.200 -wrap+ -cbox5-51o 0.5,1.0,7.0,5.2 -cbox2-3,5,9,10- 0.5,1.5,9.0,7.0 -ehl 1 -evl 1 -sm -dev kp3 -a- -ui- -x'
#     frame.cleaning_command_line_from_cbox()
#     assert frame.strvar_command_args == result
#     frame.strvar_command_args = '-mode def -rt 0 -ws 0.200 -wrap+ -cbox5-51o 0.5,1.0,7.0,5.2 -cbox2-3,5,9,10- 0.5,1.5,9.0,7.0 -cbox2-52e,3-33o 0.8,0.5,8.0,8.0 -cbox2-5e,3-7o,9- 0.5,1.5,9.0,7.0 -ehl 1 -evl 1 -sm -dev kp3 -a- -ui- -x'
#     frame.cleaning_command_line_from_cbox()
#     assert frame.strvar_command_args == result
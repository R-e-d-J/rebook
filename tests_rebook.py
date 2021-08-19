# Test
import rebook

def test_command_arguments_string_generation():
    assert "-a- ui- -x" in rebook.generate_command_argument_string()
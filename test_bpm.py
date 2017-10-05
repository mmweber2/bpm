import bpm
# Rolling backport of unittest.mock for Python 2
from mock import patch
from nose.tools import assert_equals

#@patch('__builtin__.raw_input')
#def test_no_beats(test_mock):
#    test_mock.return_value = "cat empty_file.txt"
#    print bpm.main()

@patch('__builtin__.raw_input')
def test_no_beats_from_stdin(test_mock):
    test_mock.side_effect = EOFError()
    assert_equals(bpm.read_beats(), [])
    
# Test:
# No beats
# 1 beat
# 2 beats
# Some beats are the same
# All beats are the same
# No bpm given
# 0 bpm given
# BPM that ranges over 0
# Negative bpm given
# No offset given
# Negative offset
# 0 offset given
# Offset that ranges over 0
# Irregular bpm song
# Non-float beats
# Non-float offset
# Non-float bpm
# What to do when score is 0?
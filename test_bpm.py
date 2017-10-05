import bpm
# Rolling backport of unittest.mock for Python 2
from mock import patch
from nose.tools import assert_equals

# Read beats expects a list of stdin beats, plus an EOFError
def simulate_beat_input(beats):
    for beat in beats:
        yield float(beat)
    raise EOFError()

# TODO: Use simulate_beat_input
@patch('__builtin__.raw_input')
def test_read_beats_no_beats(test_mock):
    test_mock.side_effect = EOFError()
    assert_equals(bpm.read_beats(), [])

@patch('__builtin__.raw_input')
def test_single_beat_from_stdin(test_mock):
    test_mock.side_effect = simulate_beat_input(["0.2"])
    assert_equals(bpm.read_beats(), [0.2])
    
# Test:
# No beats (from file?)
# 1 beat
# 2 beats
# Non-float beat(s)
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
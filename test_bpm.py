import bpm
# Rolling backport of unittest.mock for Python 2
from mock import patch
from nose.tools import assert_equals
from nose.tools import assert_raises

# Read beats expects a list of stdin beats, plus an EOFError
def simulate_beat_input(beats):
    for beat in beats:
        yield beat
    raise EOFError()

@patch('__builtin__.raw_input')
def test_read_beats_no_beats(test_mock):
    test_mock.side_effect = simulate_beat_input([])
    assert_equals(bpm.read_beats(), [])

@patch('__builtin__.raw_input')
def test_read_beats_single_beat(test_mock):
    test_mock.side_effect = simulate_beat_input(["0.2"])
    assert_equals(bpm.read_beats(), [0.2])
    
@patch('__builtin__.raw_input')
def test_read_beats_two_beats(test_mock):
    test_mock.side_effect = simulate_beat_input(["0.2", "1.5"])
    assert_equals(bpm.read_beats(), [0.2, 1.5])

@patch('__builtin__.raw_input')
def test_read_beats_non_float_beat(test_mock):
    test_mock.side_effect = simulate_beat_input(["s"])
    assert_raises(ValueError, bpm.read_beats)

@patch('__builtin__.raw_input')
def test_read_beats_float_and_non_float_beats(test_mock):
    test_mock.side_effect = simulate_beat_input(["0.5", "1", "s"])
    assert_raises(ValueError, bpm.read_beats)

# Test:
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
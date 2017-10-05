import bpm
# Rolling backport of unittest.mock for Python 2
from mock import patch
from nose.tools import assert_equals
from nose.tools import assert_raises

# Read beats expects a list of stdin beats, ending in an EOFError
def simulate_beat_input(beats):
    for beat in beats:
        yield beat
    raise EOFError()

# Tests for read_beats
@patch('__builtin__.raw_input')
def test_read_beats_no_beats(test_mock):
    test_mock.side_effect = simulate_beat_input([])
    assert_equals(bpm.read_beats(), [])

@patch('__builtin__.raw_input')
def test_read_beats_single_beat(test_mock):
    test_mock.side_effect = simulate_beat_input(["0.2"])
    assert_equals(bpm.read_beats(), [0.2])

# A negative result will cause errors in other parts of bpm,
#   but read_beats shouldn't treat it differently
@patch('__builtin__.raw_input')
def test_read_beats_negative_beat(test_mock):
    test_mock.side_effect = simulate_beat_input(["-0.2"])
    assert_equals(bpm.read_beats(), [-0.2])
    
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

# Test get_bpms
def test_get_bpms_empty():
    beats = []
    assert_equals(bpm.get_bpms(beats), [])

def test_get_bpms_one_beat():
    beats = [1.0]
    assert_equals(bpm.get_bpms(beats), [])

def test_get_bpms_duplicate_beats():
    beats = [0.2, 0.2]
    assert_raises(ValueError, bpm.get_bpms, beats)

def test_get_bpms_some_duplicate_beats():
    beats = [0.2, 0.5, 0.5]
    assert_raises(ValueError, bpm.get_bpms, beats)

def test_get_bpms_decreasing_beats():
    beats = [0.2, 0.5, 0.1]
    assert_raises(ValueError, bpm.get_bpms, beats)

def test_get_bpms_negative_beat():
    beats = [0.2, 0.5, -0.1]
    assert_raises(ValueError, bpm.get_bpms, beats)

def test_get_bpms_negative_beat_first():
    beats = [-0.5, 0.2, 0.5]
    assert_raises(ValueError, bpm.get_bpms, beats)

def test_get_bpms_beat_at_zero():
    beats = [0.0, 0.3]
    assert_equals(bpm.get_bpms(beats), [200.0])

def test_get_bpms_unique_beats_same_bpm():
    beats = [0.2, 0.5, 0.8]
    assert_equals(bpm.get_bpms(beats), [200.0])

def test_get_bpms_unique_beats_different_bpms():
    beats = [0.2, 0.5, 0.7, 0.85]
    assert_equals(bpm.get_bpms(beats), [200.0, 300.0, 400.0])

# Tests for score_accuracy
def test_score_accuracy_below_one():
    # Test above and below 1 to guard against a bug where the latest
    #   beat was rounded down to 0, causing an empty expected beat list
    beats = [0.2, 0.5, 0.7, 0.85]
    # Rather than testing for a specific score, try to find a score
    #    that makes sense
    assert bpm.score_accuracy(beats, 200.0) > 0
    assert bpm.score_accuracy(beats, 300.0) > 0
    assert bpm.score_accuracy(beats, 400.0) > 0

def test_score_accuracy_above_one():
    beats = [1.2, 2.5, 3.7, 4.85]
    assert bpm.score_accuracy(beats, 200.0) > 0
    assert bpm.score_accuracy(beats, 300.0) > 0
    assert bpm.score_accuracy(beats, 400.0) > 0

def test_score_accuracy_relative():
    # BPM should be 200.0
    beats = [0.2, 0.5, 0.8]
    assert bpm.score_accuracy(beats, 200.0) > bpm.score_accuracy(beats, 150.0)

def test_score_accuracy_accurate_bpm():
    # BPM should be 60.0
    beats = [1, 2, 3]
    assert_equals(bpm.score_accuracy(beats, 60), 0)

def test_score_accuracy_slow_bpm():
    # BPM should be 60.0
    beats = range(10)
    assert_equals(bpm.score_accuracy(beats, 30), 0)

def test_score_accuracy_zero_bpm():
    beats = [0.2, 0.5, 0.8]
    assert_raises(ValueError, bpm.score_accuracy, beats, 0)

def test_score_accuracy_negative_bpm():
    beats = [0.2, 0.5, 0.8]
    assert_raises(ValueError, bpm.score_accuracy, beats, -10)

def test_score_accuracy_too_large_offset():
    beats = [0.2, 0.5, 0.8]
    assert_raises(ValueError, bpm.score_accuracy, beats, 200, 1)


# Test:
# Find_bpm
# Score accuracy
# Main() and __main__
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
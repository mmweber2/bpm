from StringIO import StringIO
import bpm
import argparse
import sys
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

def test_score_accuracy_no_beats():
    assert_raises(ValueError, bpm.score_accuracy, [], 60)

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
    beats = [1, 2, 3, 4, 5]
    assert_equals(bpm.score_accuracy(beats, 60), 0)

# TODO: Add test for multiple of exact bpm

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

# Tests for find_bpm

def test_find_bpm_zero_bpm():
    assert_raises(ValueError, bpm.find_bpm, range(5), 0, 0)

def test_find_bpm_negative_bpm():
    assert_raises(ValueError, bpm.find_bpm, range(5), -100, 0)

def test_find_bpm_non_numeric_bpm():
    assert_raises(TypeError, bpm.find_bpm, range(10), "Test", 0)

def test_find_bpm_small_bpm():
    # This is a possible bpm that should return valid results
    assert bpm.find_bpm(range(100), 10, 0) != ""

def test_find_bpm_exact_bpm():
    # find_bpm's OFFSET_LIMIT and BPM_VARIANCE will affect the
    #   best matches returned, and the score will change
    #   with any changes to the scoring system.
    # For now, just look for any results.
    assert bpm.find_bpm(range(100), 60, 0) != ""

def test_find_bpm_negative_offset():
    assert_raises(ValueError, bpm.find_bpm, range(5), 60, -10)

# Zero offset is the default and is tested by some of the above tests

def test_find_bpm_small_offset():
    # This is a possible offset that should return valid results
    assert bpm.find_bpm(range(100), 60, .0000001) != ""

def test_find_bpm_too_large_offset():
    # Offset is larger than last beat
    assert_raises(ValueError, bpm.find_bpm, range(100), 60, 100)

def test_find_bpm_valid_large_offset():
    assert bpm.find_bpm(range(100), 60, 50) != ""

def test_find_bpm_non_numeric_offset():
    assert_raises(TypeError, bpm.find_bpm, range(10), 60, "Test")

@patch('bpm.read_beats', return_value=[])
@patch('sys.stdout', new_callable=StringIO)
def test_main_no_beats(print_mock, beats_mock):
    bpm.main()
    assert_equals(print_mock.getvalue(), "No beats found.\n")

def is_valid_score(test_mock):
    '''Checks the mock's value against the expected score.

    Returns True iff the value begins with the expected value.
    '''
    bpm.main()
    expected = "\nBPM " # Valid start to any score list
    #sys.stderr.write("Result was {}".format(test_mock.getvalue()))
    return test_mock.getvalue().startswith(expected)

@patch('bpm.read_beats', return_value=range(60))
@patch('sys.stdout', new_callable=StringIO)
def test_main_no_args_given(print_mock, beats_mock):
    assert is_valid_score(print_mock)
    
@patch('bpm.read_beats', return_value=range(60))
@patch('sys.stdout', new_callable=StringIO)
def test_main_negative_offset_given(print_mock, beat_mock):
    with patch('sys.argv', (None, "-10", "60")):
        assert is_valid_score(print_mock)

@patch('bpm.read_beats', return_value=range(60))
@patch('sys.stdout', new_callable=StringIO)
def test_main_zero_offset_given(print_mock, beat_mock):
    with patch('sys.argv', (None, "0", "60")):
        assert is_valid_score(print_mock)

@patch('bpm.read_beats', return_value=range(60))
@patch('sys.stdout', new_callable=StringIO)
def test_main_positive_offset_given(print_mock, beat_mock):
    with patch('sys.argv', (None, "5", "60")):
        assert is_valid_score(print_mock)

@patch('bpm.read_beats', return_value=range(60))
def test_main_non_float_offset_given(beat_mock):
    with patch('sys.argv', (None, "Test", "60")):
        assert_raises(ValueError, bpm.main)

# Zero, negative, and near-zero bpms are tested in find_bpm
#   and aren't checked in main()

# Test this in main because there is a float conversion
def test_main_non_float_bpm_given():
    pass
    
    #parser = argparse.ArgumentParser()
    #parser.add_argument('0') # Offset
    #parser.add_argument('60') # BPM

# Test:
# Main() and __main__
# No bpm given
# 0 bpm given
# Irregular bpm song
import sys
from itertools import count

# Usage: python bpm.py (input)
# where (input) is a stdin list of beats

# TODO: Start with greedy algorithm, then find better
# TODO: Replace new_error (for troubleshooting) with increments to total_error
# TODO: Break into smaller functions
# TODO: Is there a better way to get the song duration?
# TODO: Find a way to use count() to generate expected beats, but with the option
#    to look at neighboring beats to find the closest one
# TODO: Handle leftover beats in both sets at the end of loop
# TODO: Do something with skipped and extra beats
def score_accuracy(beat_set, bpm, offset=0.0, verbose=False):
    '''Scores a bpm given a set of beats.

    Given the bpm and offset, calculates the expected location for each beat,
    matches it to the closest unmatched beat, and adds the squared difference
    to the total error.
    The lower the total error, the better a match the bpm for that beat set.

    Args:
        beat_set: List of floats, where each float in the list represents a
            detected or confirmed beat.
        bpm: Float, the estimated bpm for the song.
        offset: Float, the location (in seconds) at which the song starts. Defaults to 0.0.
        verbose: Boolean, whether or not to show debug output.

    Returns:
        The sum of the squared errors for the beat set.
    '''
    beat_interval = 60.0 / bpm
    duration = int(beat_set[-1])
    # Aubio does not seem to detect beats in the first 3 seconds, so try this workaround
    last_beat = offset + 3.0
    expected_beats = []
    # If bpm is 30 and offset is 0, this should place beats at 2, 4, 6, etc
    while last_beat <= duration:
        expected_beats.append(last_beat)
        last_beat += beat_interval
    total_error = 0
    rb_index = 1 # Real beat index (from beat_set)
    eb_index = 1 # Expected beat index
    skipped_beats = [] # Beats in beat_set but not in expected
    extra_beats = [] # Beats in expected but not in beat_set
    while rb_index < len(beat_set) and eb_index < len(expected_beats):
        expected_beat = expected_beats[eb_index]
        if eb_index < len(expected_beats) - 1 and expected_beats[eb_index + 1] <= beat_set[rb_index]:
            # Extra expected beat (or, a missing beat in beat_set),
            #   because the next expected beat is closer to the next real beat than this one is
            # This could happen if a real beat is not detected, or the bpm is way off.
            extra_beats.append(expected_beat)
            # Try to move eb_index closer to the next actual beat
            eb_index += 1
            continue
        if (beat_set[rb_index-1] < expected_beat <= beat_set[rb_index]):
            # Beat is close to being on target
              total_error += (beat_set[rb_index] - expected_beat)**2
              eb_index += 1
              rb_index += 1
        else:
            # Skipped beat: a beat in beat_set is not accounted for in expected_beats
            skipped_beats.append(beat_set[rb_index])
            rb_index += 1
            if verbose: print "Found skipped beat ", beat_set[rb_index]
    return total_error

def find_bpm(start_bpm, start_offset):
    """Returns the top scoring bpm and offset pairs for the given song."""
    TOP_SCORES = 20
    # FIXME: Set these back to 1 maybe
    OFFSET_LIMIT = .2
    BPM_VARIANCE = .2
    scores = []
    # TODO: Adjust starting points of bpm and offset?
    for bpm in count(start_bpm - BPM_VARIANCE, .001):
        for offset in count(start_offset - OFFSET_LIMIT, .01):
            total_error = score_accuracy(beats, bpm, offset)
            scores.append((total_error, bpm, offset))
            if offset > start_offset + OFFSET_LIMIT: break
        if bpm > start_bpm + BPM_VARIANCE: break
    scores.sort()
    return "\n".join(map(str, scores[:TOP_SCORES]))

def read_beats():
    """Reads in a list of floating point beats from stdin."""
    beats = []
    while True:
        try:
            beat = raw_input()
        except EOFError:
            return beats
        beats.append(float(beat))
    # Should not reach here, but just in case
    return beats

def get_bpms(beat_set):
    """Returns a sorted list of possible BPMs from a beat set."""
    bpms = []
    # Each possible BPM is calculated by the difference from the last beat
    # 3.5 - 3.0 = .5: 60 / .5 = 120 BPM
    for i in xrange(1, len(beat_set)):
        bpms.append(60.0 / (beats[i] - beats[i-1]))
    bpms.sort()
    return bpms

beats = read_beats()
print "Beat count is", len(beats)
input_bpm = float(sys.argv[1])
input_offset = float(sys.argv[2])
# Test a single BPM
#print score_accuracy(beats, input_bpm, input_offset)
print find_bpm(input_bpm, input_offset)
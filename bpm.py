import sys
from itertools import count

# Usage: python bpm.py (input)
# where (input) is a stdin list of beats

# TODO: Start with greedy algorithm, then find better
# TODO: Replace new_error (for troubleshooting) with increments to total_error
# TODO: Break into smaller functions
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
    # TODO: Is there a better way to get the song duration?
    duration = int(beat_set[-1])
    # TODO: Find a way to use count(), but with the option to look at neighboring beats to find the closest one
    # Aubio does not seem to detect beats in the first 3 seconds, so try this workaround
    last_beat = offset + 3.0
    expected_beats = []
    # If bpm is 30 and offset is 0, this should place beats at 2, 4, 6, etc
    while last_beat <= duration:
        expected_beats.append(last_beat)
        last_beat += beat_interval
    total_error = 0
    # Real beat index (from beat_set)
    rb_index = 1
    # Expected beat index
    eb_index = 1
    # TODO: Handle leftover beats in both sets at the end of loop
    # TODO: Do something with skipped and extra beats

    # Beats in beat_set but not in expected
    skipped_beats = []
    # Beats in expected but not in beat_set
    extra_beats = []
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

def find_bpm(input_bpm, input_offset):
    OFFSET_LIMIT = .5
    BPM_VARIANCE = 1
    scores = []
    # TODO: Adjust starting points of bpm and offset?
    for bpm in count(input_bpm - 2, .01):
        for offset in count(input_offset - 1, .01):
            total_error = score_accuracy(beats, bpm, offset)
            scores.append((total_error, bpm, offset))
            if offset > input_offset + OFFSET_LIMIT: break
        if bpm > input_bpm + BPM_VARIANCE: break
    scores.sort()
    return "\n".join(map(str, scores[:20]))

def read_beats():
    beats = []
    while True:
        try:
            beat = raw_input()
        except EOFError:
            return beats
        beats.append(float(beat))
    # Should not reach here, but just in case
    return beats

beats = read_beats()
beat_count = len(beats)
print "Beat count is", beat_count
# 137, .168
input_bpm = float(sys.argv[1])
input_offset = float(sys.argv[2])
print find_bpm(input_bpm, input_offset)
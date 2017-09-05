import sys

# Usage: python bpm.py (input)
# where (input) is a stdin list of beats

# TODO: Start with greedy algorithm, then find better
def score_accuracy(beat_set, bpm, offset=0):
    '''Scores a bpm given a set of beats.

    Given the bpm and offset, calculates the expected location for each beat,
    matches it to the closest unmatched beat, and adds the squared difference
    to the total error.
    The lower the total error, the better a match the bpm for that beat set.

    Args:
        beat_set: List of floats, where each float in the list represents a
            detected or confirmed beat.
        bpm: Float, the estimated bpm for the song.
        offset: Float, the location (in seconds) at which the song starts.

    Returns:
        The sum of the squared errors for the beat set.
    '''
    beat_interval = 60 / bpm
    # TODO: Find better way to get song duration
    duration = int(beat_set[-1])
    # If bpm is 30 and offset is 0, this should place beats at 2, 4, 6, etc
    expected_beats = range(offset, duration + 1, beat_interval)
    total_error = (expected_beats[0] - beats[0])**2
    # TODO: The same beat can no longer be used twice, but experiment with a smarter way to match beats
    # Real beat index (from beat_set)
    rb_index = 1
    # Expected beat index
    eb_index = 1
    # TODO: Handle missed beats
    while rb_index < len(beat_set):
        expected_beat = expected_beats[eb_index]
        if eb_index < len(expected_beats) - 1 and expected_beats[eb_index + 1] <= beat_set[rb_index]:
            # Extra expected beat
            # TODO: How to score extra beats?
            new_error = min(expected_beat - beat_set[rb_index-1], beat_set[rb_index] - expected_beat)**2
            print "Adding extra beat: ", new_error
            total_error += new_error
            eb_index += 1
            continue
        if (beat_set[rb_index-1] < expected_beat <= beat_set[rb_index]):
            new_error = (beat_set[rb_index] - expected_beat)**2
            #total_error += (beat_set[beat_index] - expected_beat)**2
            total_error += new_error
            print "After comparing beats {}, {}, and {}, adding error {}".format(beat_set[rb_index-1], expected_beat, beat_set[rb_index], new_error)
            eb_index += 1
        # Advance the beat we're comparing to whether or not we found one
        rb_index += 1
    print "Expected:"
    print expected_beats
    print "Actual:"
    print beat_set 
    print "Total error is ", total_error


beat = 0
beats = []
while beat is not None:
    beats.append(float(beat))
    try:
        beat = raw_input()
    except EOFError:
        break
beat_count = len(beats)
print "Beat count is", beat_count

score_accuracy(beats, 60)
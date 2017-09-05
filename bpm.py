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
    # TODO: This doesn't worry about if the beat has already been matched, fix that
    beat_index = 1
    for i in xrange(1, len(expected_beats)):
        expected_beat = expected_beats[i]
        while not(beat_set[beat_index-1] < expected_beat <= beat_set[beat_index]):
            beat_index += 1
        new_error = (beat_set[beat_index] - expected_beat)**2
        #total_error += (beat_set[beat_index] - expected_beat)**2
        print "After comparing beats {}, {}, and {}, adding error {}".format(beat_set[beat_index-1], expected_beat, beat_set[beat_index], new_error)
    print "Expected:"
    print expected_beats
    print "Actual:"
    print beat_set 
    print total_error

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
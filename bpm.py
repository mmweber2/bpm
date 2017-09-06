import sys

# Usage: python bpm.py (input)
# where (input) is a stdin list of beats

# TODO: Start with greedy algorithm, then find better
# TODO: Replace new_error (for troubleshooting) with increments to total_error
# TODO: Break into smaller functions
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
    beat_interval = 60.0 / bpm
    # TODO: Find better way to get song duration
    duration = int(beat_set[-1])
    # If bpm is 30 and offset is 0, this should place beats at 2, 4, 6, etc
    # TODO: This only places integer beats
    expected_beats = []
    last_beat = offset
    while last_beat < duration + 1:
        new_beat = last_beat + beat_interval
        expected_beats.append(new_beat)
        last_beat = new_beat
    total_error = (expected_beats[0] - beats[0])**2
    # TODO: The same beat can no longer be used twice, but experiment with a smarter way to match beats
    # Real beat index (from beat_set)
    rb_index = 1
    # Expected beat index
    eb_index = 1
    # Location of last actual beat that did not match to an expected beat
    last_skipped_beat = 0
    # TODO: Handle leftover beats in both sets at the end of loop
    while rb_index < len(beat_set) and eb_index < len(expected_beats):
        expected_beat = expected_beats[eb_index]
        if eb_index < len(expected_beats) - 1 and expected_beats[eb_index + 1] <= beat_set[rb_index]:
            # Extra expected beat (or, a missing beat in beat_set),
            #   because the next expected beat is closer to the next real beat than this one is
            # This could happen if a real beat is not detected, or the bpm is way off.
            # TODO: How to score extra beats?
            new_error = min(expected_beat - beat_set[rb_index-1], beat_set[rb_index] - expected_beat)**2
            print "Adding error from extra beat: ", new_error
            total_error += new_error
            # Try to move eb_index closer to the next actual beat
            eb_index += 1
            continue
        if (last_skipped_beat < expected_beat <= beat_set[rb_index]):
            # This expected beat is between the last skipped beat
            #   and the next actual beat.
            # Compare the distance between this beat and the next beat to
            # this beat vs the last skipped beat.
            # If the last skipped beat is closer, reset it and don't move rb_index.
            # Otherwise, use this beat and advance rb_index.
            # TODO: This could cause "hopscotching" over beats due to not resetting the
            # last skipped beat, fix that
            if expected_beat - last_skipped_beat < beat_set[rb_index] - expected_beat:
                new_error = (expected_beat - last_skipped_beat)**2
                print "Using a skipped beat"
                # Don't use this skipped beat again
                last_skipped_beat = 0
                print "Adding error from using skipped beat: ", new_error
                total_error += new_error
                # This expected beat has now been accounted for
                eb_index += 1
                continue
            else:
                print "Using the following beat"
                new_error = (beat_set[rb_index] - expected_beat)**2
            total_error += new_error
            eb_index += 1
        else:
            # Skipped beat: a beat in beat_set is not accounted for in expected_beats
            last_skipped_beat = beat_set[rb_index]
            rb_index += 1
            print "Skipped beat ", last_skipped_beat
            total_error += (last_skipped_beat - beat_set[rb_index - 1])**2
            # TODO: How to score skipped beats?
            # Temporarily, I'll use (skipped beat) - (previous beat) squared
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

score_accuracy(beats, 120)
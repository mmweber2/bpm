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
    print "Expected:"
    print expected_beats
    print "Actual:"
    print beat_set 

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

# Try subtracting first beat to get a more accurate average
# Any time in the song after the last beat is also skipped
song_secs = beats[-1] - beats[0]
#print "Song is {} seconds long".format(song_secs)
score_accuracy(beats, 60)
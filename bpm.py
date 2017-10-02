import sys
from itertools import count

# Usage: python bpm.py (input) ()
# where (input) is a stdin list of beats

def score_accuracy(beat_set, bpm, offset=0.0):
    """Scores a bpm and offset pair for a given set of beats.

    Given the bpm and offset, calculates the expected location for each beat,
    matches it to the closest unmatched beat, and adds the squared difference
    to the total error.
    The lower the total error, the better a match the bpm for that beat set.

    Args:
        beat_set: List of floats, where each float in the list represents a
            detected or confirmed beat.
        bpm: Float, the estimated bpm for the song.
        offset: Float, the location (in seconds) at which the song starts.
            Defaults to 0.0.

    Returns:
        The sum of the squared errors for the beat set.
    """
    duration = int(beat_set[-1])
    beat_interval = 60.0 / bpm
    expected_beats = []
    # Latest beat (to start, this is just the location of the first beat)
    last_beat = offset
    # If bpm is 30 and offset is 0, this should place beats at 2, 4, 6, etc
    while last_beat <= duration:
        expected_beats.append(last_beat)
        last_beat += beat_interval
    total_error = 0
    rb_index = 1 # Real beat index (from beat_set)
    eb_index = 1 # Expected beat index
    # The following lists are kept for reference only, with no effect on score
    skipped_beats = [] # Beats in beat_set but not in expected
    extra_beats = [] # Beats in expected but not in beat_set
    while rb_index < len(beat_set) and eb_index < len(expected_beats):
        expected_beat = expected_beats[eb_index]
        if (eb_index < len(expected_beats) - 1 and
            expected_beats[eb_index + 1] <= beat_set[rb_index]):
            # Extra expected beat (or, a missing beat in beat_set),
            #   because the next expected beat is closer to the next real beat.
            # This could happen if a real beat is not detected,
            #   or the bpm is way off.
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
            # A beat in beat_set is not accounted for in expected_beats
            skipped_beats.append(beat_set[rb_index])
            rb_index += 1
    # Disregard any leftover beats in either set.
    return total_error

def find_bpm(beats, start_bpm, start_offset):
    """Returns the top scoring bpm and offset pairs for the given song.

    Examines BPMs and offsets in the space around the start values to find
        the most likely BPM/offset pair.

    Args:
        beats: List of floats, where each float in the list represents a
            detected or confirmed beat.
        start_bpm: Float, the middle of the BPM range to search.
        start_offset: Float, the middle of the possible locations (in seconds)
            for which to search for an offset.
        
    Returns:
        A string in the format "(error, 'bpm', 'offset')\n", where error is
            the calculated error for that bpm/offset pairing and bpm and offset
            are the values to achieve that score.
        Results are sorted by increasing score, so the best-ranked results
            are at the top of the list.
        bpm and offset are enclosed in single quotes, and truncated
            to 5 digits after the decimal point.
    """
    TOP_SCORES = 20
    OFFSET_LIMIT = .5
    BPM_VARIANCE = 1
    scores = []
    # Per count() documentation, this format can lead to better
    #      floating point accuracy than using a float step
    for offset in (start_offset - OFFSET_LIMIT + .01 * i for i in count()):
        for bpm in (start_bpm - BPM_VARIANCE + .001 * i for i in count()):
            total_error = score_accuracy(beats, bpm, offset)
            scores.append((total_error, "{:.5f}".format(bpm), "{:.5f}".format(offset)))
            if bpm > start_bpm + BPM_VARIANCE: break
        if offset > start_offset + OFFSET_LIMIT: break
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
    offset = 0 - beat_set[0]
    # Each possible BPM is calculated by the difference from the last beat
    # 3.5 - 3.0 = .5: 60 / .5 = 120 BPM
    for i in xrange(1, len(beat_set)):
        bpms.append(60.0 / (beats[i] - beats[i-1]))
    bpms.sort()
    return bpms

def main():
    beats = read_beats()
    if len(sys.argv) > 1:
        offset = float(sys.argv[1])
    else:
        # Detected difference for Aubio with hop limit 100; remove if not using Aubio
        offset = beats[0] - 2.2
    if len(sys.argv) > 2:
        start_bpm = float(sys.argv[2])
    else:
        # Choose 25% lowest BPM for start point
        start_bpm = get_bpms(beats)[int(len(beats) * .25)]
    print find_bpm(beats, start_bpm, offset)

if __name__ == "__main__":
    main()
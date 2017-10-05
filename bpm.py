import sys
from itertools import count

# Usage: python bpm.py (input) (offset) (bpm)
#   where (input) is a stdin list of beats,
#   (offset) is a float of the location (in seconds) at which
#       the song starts, 
#   and (bpm) is an estimated bpm.
# (offset) and (bpm) are both optional.

def score_accuracy(beat_set, bpm, offset=0.0):
    """Scores a bpm and offset pair for a given set of beats.

    Given the bpm and offset, calculates the expected location for each beat,
    matches it to the closest unmatched beat, and adds the squared difference
    to the total error.
    The lower the total error, the better the match the bpm for that beat set.

    Args:
        beat_set: List of floats, where each float in the list represents a
            detected or confirmed beat. Must not be empty.
        bpm: Float, the estimated bpm for the song. Must be >= 0.
        offset: Float, the location (in seconds) at which the song starts.
            Defaults to 0.0. Must be less than the last beat of beat_set.

    Returns:
        The sum of the squared errors for the beat set.

    Raises:
        ValueError: bpm is <= 0, offset is >= the last beat, or
            beat_set is empty.
    """
    if not beat_set:
        raise ValueError("beat_set must not be empty")
    if bpm <= 0:
        raise ValueError("bpm must be greater than 0")
    duration = beat_set[-1]
    if duration <= offset:
        # If offset is >= duration, there will be no beats to compare,
        #    causing an erroneous 0.0 return
        raise ValueError("No beats found after offset")
    beat_interval = 60.0 / bpm
    expected_beats = []
    # Latest beat (to start, this is just the location of the first beat)
    last_beat = offset
    # If bpm is 30 and offset is 0, this should place beats at 2, 4, 6, etc
    while last_beat <= duration:
        expected_beats.append(last_beat)
        # Offset floating point errors by rounding
        last_beat = round(beat_interval + last_beat, 7)
    total_error = 0
    rb_index = 1 # Real beat index (from beat_set)
    eb_index = 1 # Expected beat index
    while rb_index < len(beat_set) and eb_index < len(expected_beats):
        expected_beat = expected_beats[eb_index]
        if (eb_index < len(expected_beats) - 1 and
            expected_beats[eb_index + 1] <= beat_set[rb_index]):
            # Extra expected beat (or, a missing beat in beat_set),
            #   because the next expected beat is closer to the next real beat.
            # This could happen if a real beat is not detected,
            #   or the bpm is way off.
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
        start_bpm: Float, the middle of the BPM range to search. Must be >= 0.
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

    Raises:
        ValueError: bpm is <= 0 or offset < 0.
    """
    TOP_SCORES = 20
    #OFFSET_LIMIT = .5 
    # TODO: Fix after testing
    OFFSET_LIMIT = .001
    # TODO: Fix after testing
    # BPM_VARIANCE = 1
    BPM_VARIANCE = 0.05
    scores = []
    # Per count() documentation, this format can lead to better
    #      floating point accuracy than using a float step
    for offset in (start_offset - OFFSET_LIMIT + .01 * i for i in count()):
        if offset < 0:
            continue
        for bpm in (start_bpm - BPM_VARIANCE + .001 * i for i in count()):
            if bpm <= 0:
                continue
            total_error = score_accuracy(beats, bpm, offset)
            scores.append((total_error, "{:.5f}".format(bpm), "{:.5f}".format(offset)))
            if bpm > start_bpm + BPM_VARIANCE:
                break
        if offset > start_offset + OFFSET_LIMIT:
            break
    scores.sort()
    return _format_results(scores[:TOP_SCORES])

def _format_results(results):
    output = ""
    for score, bpm, offset in results:
        line = "\nBPM {} with offset {} (score: {})".format(bpm, offset, score)
        output += line
    return output

def read_beats():
    """Reads in a list of beats from stdin.
    
    Returns: A list of floats representing beats.

    Raises:
        ValueError: one or more beats cannot be converted to a float.
    """
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
    """Returns a sorted list of possible BPMs from a beat set.

    If beat_set contains less than two unique values, returns an empty list.
    
    Input:
        beat_set: a sorted (increasing) list of floats representing beats.

    Returns:
        A list of estimated floating point BPM values, sorted in increasing order.

    Raises:
        ValueError: beat_set is not in increasing order.
    """
    bpms = []
    # Each possible BPM is calculated by the difference from the last beat
    # 3.5 - 3.0 = .5: 60 / .5 = 120 BPM
    seen_bpms = set()
    for i in xrange(1, len(beat_set)):
        # Due to Python floating point errors, the same beat difference may
        #    be represented slightly differently, so round to 7 decimal places.
        # This should be sufficient to maintain accuracy yet avoid the errors.
        beat_difference = round(beat_set[i] - beat_set[i-1], 7)
        if beat_difference <= 0:
            # This should not happen normally, but may mean the data is flawed
            raise ValueError("Beats not in increasing order")
        elif beat_difference > round(beat_set[i], 7):
            raise ValueError("Beats may not be negative")
        bpm = 60.0 / beat_difference
        if bpm not in seen_bpms:
            bpms.append(bpm)
            seen_bpms.add(bpm)
    bpms.sort()
    return bpms

def main():
    beats = read_beats()
    if not beats:
        print "No beats found."
        return
    if len(sys.argv) > 1:
        # User-supplied offsets are negative or zero by convention
        offset = 0 - float(sys.argv[1])
        print "Setting offset: ", offset
    else:
        # Detected difference for Aubio with hop limit 100; remove if not using Aubio
        offset = beats[0] - 2.2
    if len(sys.argv) > 2:
        start_bpm = float(sys.argv[2])
        print "Setting start bpm: ", start_bpm
    else:
        # Choose 25% lowest BPM for start point
        start_bpm = get_bpms(beats)[int(len(beats) * .25)]
    print find_bpm(beats, start_bpm, offset)

if __name__ == "__main__":
    main()
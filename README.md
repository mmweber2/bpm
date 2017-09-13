# steps

This program can be used to estimate song BPMs and starting offsets.

It is not intended for songs with variable BPMs, and may give inaccurate results
in such cases.

Usage:
python bpm.py (input) (offset) (bpm)
Where (input) is a stdin list of beats.

One tool that provides such a list of beats is Aubio's aubiotrack command:
https://aubio.org
However, its results are not exact, and are affected by the hop limit option.
Setting the hop limit lower (<= 100) seems to give more accurate results, but
takes much longer to compute.

The (offset) and (bpm) values are optional, and can be used if an approximate
offset and bpm are already available. The offset option can be used without
a starting bpm, but the bpm setting cannot be used without an offset.

# steps

This program can be used to estimate song BPMs and starting offsets.

It is not intended for songs with variable BPMs, and may give inaccurate results
in such cases.

Usage:
python bpm.py (input) (offset) (bpm)
Where (input) is a stdin list of floating-point beat locations,
(offset) is a floating-point of the location (in seconds) at which
the song starts, and (bpm) is an estimated bpm.

The (offset) and (bpm) values are optional, and can be used if an approximate
offset and bpm are already available. If only one additional number is provided,
it will be interpreted as an offset, since the offset is easier to guess manually.

This results in output of the format:

Scores of 0 are usually suspect, but are possible if the music is very regular.

This program does not consider quarter beats or other beats outside of the full beat mark,
so it does not recognize 30 or 120 bpm as equivalent to 60 bpm.


One tool that provides such a list of beats is Aubio's aubiotrack command:
https://aubio.org
However, its results are not exact, and are affected by the hop limit option.
Setting the hop limit lower (<= 100) seems to give more accurate results, but
takes much longer to compute.

Raises:
    ValueError: offset or bpm are not valid floating point numbers.
# steps

This program can be used to estimate song BPMs.

It is not intended for songs with variable BPMs, and may throw an error in such cases.

Usage:
python bpm.py (input)
Where (input) is a stdin list of beats.

One tool that provides such a list of beats is Aubio's aubiotrack command:
https://aubio.org
However, its results are not exact, and are affected by the hop limit option.

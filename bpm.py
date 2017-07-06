import sys

# TODO: Determine when a song varies too much to calculate

lines = []

def avg(nums):
    return sum(nums) / len(nums)

with open(sys.argv[1], 'r') as filename:
    lines = filename.readlines()
beats = [float(x) for x in lines]
# Try subtracting first beat
song_mins = (beats[-1] - beats[0]) / 60
beat_diffs = []
avg_beat_diffs = []
for i in xrange(1, len(beats)):
    beat_diffs.append(beats[i] - beats[i-1])
    if i % 4 == 0:
        avg_beat_diffs.append(sorted(beat_diffs[i-3:i+1])[1])
print "First beat is at ", beats[0]
print "Last beat is at ", beats[-1]
print "Average difference is:"
print sum(beat_diffs) / len(beat_diffs)
print "Median difference is:"
print sorted(beat_diffs)[len(beat_diffs) / 2]
num_diffs = len(avg_beat_diffs)
#overall_avg = avg(avg_beat_diffs[num_diffs / 3: num_diffs - (num_diffs / 3)])
overall_avg = avg(beat_diffs)
print "The overall avg is ", overall_avg
print "If we multiply the seconds by that average, we get ", beats[-1] * (1 - overall_avg)
print "Song is {} minutes long".format(song_mins)
print "There are {} beats in total, so that's {} bpm.".format(len(beats), len(beats) / song_mins)



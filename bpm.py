import sys


def avg(nums):
    return sum(nums) / len(nums)

# TODO: Determine when a song varies too much to calculate

lines = []

with open(sys.argv[1], 'r') as filename:
    lines = filename.readlines()
beats = [float(x) for x in lines]
beat_count = len(beats)
print "Beat count is ", beat_count

# Try subtracting first beat to get a more accurate average
# Any time in the song after the last beat is also skipped
song_secs = beats[-1] - beats[0]
print "Song is {} seconds long".format(song_secs)

# Try tracking all beat differences and average of every 4 to balance out spikes
beat_diffs = []
avg_beat_diffs = []
for i in xrange(1, len(beats)):
    beat_diffs.append(beats[i] - beats[i-1])
    if i % 4 == 0:
        avg_beat_diffs.append(sorted(beat_diffs[i-3:i+1])[1])
        
print "Average of all differences is ", avg(beat_diffs)
print "Average of average differences is ", avg(avg_beat_diffs)

print "Median difference is: ", sorted(avg_beat_diffs)[len(avg_beat_diffs) / 2]

num_diffs = len(avg_beat_diffs)
med_avg = avg(avg_beat_diffs[num_diffs / 3: num_diffs - (num_diffs / 3)])
overall_avg = avg(beat_diffs)
print "Average of median beat diffs is ", med_avg
print "Average of all beat diffs is ", overall_avg

beats_sec = 1 / med_avg
#beats_sec = 1 / overall_avg

print "Beats/sec is ", beats_sec

print "That's {} bpm.".format(beats_sec * 60)



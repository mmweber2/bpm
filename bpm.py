import sys

def avg(nums):
    return sum(nums) / len(nums)

class VariedBPMException(Exception):
    pass    

# The maximum difference in BPMs to allow before considering a song
#     too irregular
MAX_BPM_VARIANCE = 1
    
file_lines = []

with open(sys.argv[1], 'r') as filename:
    file_lines = filename.readlines()
beats = [float(x) for x in file_lines]
beat_count = len(beats)
#print "Beat count is", beat_count

# Try subtracting first beat to get a more accurate average
# Any time in the song after the last beat is also skipped
song_secs = beats[-1] - beats[0]
#print "Song is {} seconds long".format(song_secs)

# Try tracking all beat differences and average of every 4 to balance out spikes
beat_diffs = []
avg_beat_diffs = []
for i in xrange(1, len(beats)):
    beat_diffs.append(beats[i] - beats[i-1])
    if i % 4 == 0:
        avg_beat_diffs.append(sorted(beat_diffs[i-3:i+1])[1])
        
beat_diffs = sorted(beat_diffs)  
avg_beat_diffs = sorted(avg_beat_diffs)      
print "Median difference of averages is: ", avg_beat_diffs[len(avg_beat_diffs) / 2]
print "Median difference of all beats is: ", beat_diffs[len(beat_diffs) / 2]

# Discard songs with large variance in BPM
max_diff = beat_diffs[-1] - beat_diffs[0]
if max_diff > MAX_BPM_VARIANCE:
    raise VariedBPMException("Song {} varies by {} BPM.".format(arg[1], max_diff))

med_avg = avg(avg_beat_diffs)
overall_avg = avg(beat_diffs)
print "Average of median beat diffs is ", med_avg
print "Average of all beat diffs is ", overall_avg

beats_sec = 1 / med_avg

print "Beats/sec is ", beats_sec

print "From the median average, that's {} bpm.".format(beats_sec * 60)
print "From the overall average, that's {} bpm.".format(1 / overall_avg * 60)
print "Average of these two is", avg((beats_sec * 60, 1 / overall_avg * 60))



import re
all_bpms = []

with open("sm_bpms.txt", "r") as bpm_file:
    all_bpms = bpm_file.readlines()

print "We have {} lines.".format(len(all_bpms))
regular_bpms = {}
poss_bpms = {}
weird_bpms = {}
for line in all_bpms:
    try:
        title, bpm = line.split("#")
    except ValueError:
        print "Error on line ", line
    if len(bpm.split(",")) == 1:
        regular_bpms[title] = bpm
        continue
    bpms = bpm.split(",")
    if len(bpms) == 2:
        # Allow two-BPM songs if the BPMs are exactly the same
        # Format example: 0.000=160.000,4.000=160.000
        # Last BPM may have formatting on the end
        bpm2 = bpms[1].strip(";\r\n")
        if bpms[0].split("=")[1] == bpm2.split("=")[1]:
            regular_bpms[title] = bpms[0]
            continue
    print "Song {} didn't match".format(line)
    weird_bpms[title] = bpms

output = "Regular BPM files:\n"
#for song in regular_bpms:
#    output += "{} : # BPM: {}\n".format(song, regular_bpms[song])
output += "Irregular BPM files:\n"
#for song in weird_bpms:
#    output += "{} : # BPMS: {}\n".format(song, weird_bpms[song])

print "That's {} with regular BPM and {} weird ones.".format(len(regular_bpms), len(weird_bpms))

#with open("filtered_bpms.txt", "w") as output_file:
#    output_file.write(output)


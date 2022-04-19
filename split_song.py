import pandas as pd
from pydub import AudioSegment
original_song = "dark_piano_2.wav"
data = list(map(lambda x: x.strip(),open('split_data/dark_piano_2','r').read().split('\n')))
split_list = []
for i in range(len(data)):
    if len(data[i].split(":")) == 2:
        split_list.append({
            "name": data[i][6:],
            "start_time": data[i][:5],
        })
    elif len(data[i].split(":")) == 3:
        split_list.append({
            "name": data[i][8:],
            "start_time": data[i][:7],
        })
for i in range(len(split_list) - 1):
    split_list[i]["end_time"] = split_list[i + 1]["start_time"]
split_list[len(split_list) - 1]["end_time"] = "NONE"
print(split_list)
audio = AudioSegment.from_wav(original_song)
for i in split_list:
    stime = i["start_time"].split(":")
    if len(stime) == 3:
        start_time = int(stime[0]) * 3600 * 1000 + int(stime[1]) * 60 * 1000 + int(stime[2]) * 1000
    elif len(stime) == 2:
        start_time = int(stime[0]) * 60 * 1000 + int(stime[1]) * 1000
    if i["end_time"] != "NONE":
        etime = i["end_time"].split(":")
        if len(etime) == 3:
            end_time = int(etime[0]) * 3600 * 1000 + int(etime[1]) * 60 * 1000 + int(etime[2]) * 1000
        elif len(etime) == 2:
            end_time = int(etime[0]) * 60 * 1000 + int(etime[1]) * 1000
    else:
        end_time = len(audio)
    audio[start_time:end_time].export("split/"+i["name"]+".wav", format="wav")
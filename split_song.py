import pandas as pd
from pydub import AudioSegment
original_song = "song/Anxious/dark-piano.wav"
data = list(map(lambda x: x.strip(),open('split_data','r').read().split('\n')))
split_list = []
for i in range(len(data)):
    split_list.append({
        "name": data[i][6:],
        "start_time": data[i][:5],
    })
for i in range(len(split_list) - 1):
    split_list[i]["end_time"] = split_list[i + 1]["start_time"]
split_list[len(split_list) - 1]["end_time"] = "NONE"

audio = AudioSegment.from_wav(original_song)
for i in split_list:
    stime = i["start_time"].split(":")
    start_time = int(stime[0]) * 60 * 1000 + int(stime[1]) * 1000
    if i["end_time"] != "NONE":
        etime = i["end_time"].split(":")
        end_time = int(etime[0]) * 60 * 1000 + int(etime[1]) * 1000
    else:
        end_time = len(audio)
    audio[start_time:end_time].export("split/"+i["name"]+".wav", format="wav")
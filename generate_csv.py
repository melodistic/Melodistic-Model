import pandas as pd
import os

from extract_song import get_bpm

mood_list = os.listdir("extract/")

data = []

for mood in mood_list:
    song_list = os.listdir("extract/"+mood)
    song_list = sorted(song_list)
    data = data + [[song,mood,get_bpm("extract/"+mood+"/"+song)] for song in song_list]

df = pd.DataFrame(data,columns=['filename','mood','bpm'])
df.to_csv('data.csv',index=False)

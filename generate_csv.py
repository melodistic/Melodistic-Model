import pandas as pd

import os

mood_list = os.listdir("extract/")

data = []

for mood in mood_list:
    song_list = os.listdir("extract/"+mood)
    song_list = sorted(song_list)
    data = data + [[song,mood] for song in song_list]

df = pd.DataFrame(data,columns=['filename','mood'])
df.to_csv('data.csv',index=False)
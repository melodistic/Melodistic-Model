import random
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import time
import warnings
import numpy as np
warnings.filterwarnings('ignore')


df = pd.read_csv("csv_features/Chill-Slow.csv")
x = df.drop(["music_name"],axis=1)
y = df["music_name"]
total_song = 50
song_list = []
threshold = 0.1
start_index = random.randint(0,total_song)
start_song = np.array([x.loc[start_index]])
while len(song_list) < total_song:
    nbrs = NearestNeighbors(n_neighbors=21, algorithm='auto', metric="cosine").fit(x)
    start_time = time.time()
    dis, pos = nbrs.kneighbors(start_song)
    drop_index = []
    for i in range(len(dis[0])):
        if dis[0][i] > threshold:
            x = x.drop(drop_index, axis=0)
            x.reset_index(drop=True, inplace=True)
            y = y.drop(drop_index, axis=0)
            y.reset_index(drop=True, inplace=True)
            break
        else:
            song_list.append(y.loc[pos[0][i]])
            start_song = np.array([x.loc[pos[0][i]]])
            drop_index.append(pos[0][i])
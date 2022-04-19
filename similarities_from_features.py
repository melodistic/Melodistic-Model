import numpy as np
import os
import json

data = json.load(open("data.json"))

def get_similarity(audio1, audio2):
    feature1 = audio1["features"]
    feature2 = audio2["features"]
    return np.dot(feature1, feature2) / (np.linalg.norm(feature1) * np.linalg.norm(feature2))

def compare_two_audio(audio1, audio2):
    similarity = get_similarity(audio1, audio2)
    return similarity

def find_most_similar_songs(current_song, mood, existed_songs):
    next_song_lists = np.random.choice(data,size = 100)
    max_similarities = 0
    max_song = None
    for next_song in next_song_lists:
        if current_song["name"] != next_song["name"] and next_song["name"] not in existed_songs:
            similarity = compare_two_audio(current_song, next_song)
            if similarity > max_similarities:
                max_similarities = similarity
                max_song = next_song
   
    return max_song

def create_list_of_song(mood, n = 10):
    current_song = np.random.choice(data,size = 1)[0]
    song_list = [current_song["name"]]
    for _ in range(n):
        next_song = find_most_similar_songs(current_song, mood, song_list)
        song_list.append(next_song["name"])
        current_song = next_song
    print(song_list)

create_list_of_song("Chill")
import time
import numpy as np
from pydub import AudioSegment
import os
import random
import librosa

mschunk = 1000


def get_data(audio):
    samples = audio.get_array_of_samples()
    arr = np.array(samples).astype(np.float32) / 32768  # 16 bit
    arr = librosa.core.resample(arr, audio.frame_rate, 22050, res_type="kaiser_best")
    S = librosa.feature.melspectrogram(arr, sr=22050, n_mels=256)
    mels = np.log(S + 1e-9)
    bpm = round(librosa.beat.tempo(y=arr)[0],2)
    normalized_bpm = normalize_bpm(bpm)
    normalized_mel = normalize_mel(mels).flatten()
    weighted_bpm = np.array([normalized_bpm] * int(len(normalized_mel) * 2))
    return np.concatenate((weighted_bpm, normalized_mel))

def normalize_bpm(bpm):
    # Max is 200 bpm, min is 40 bpm
    return (bpm - 40) / 160 

def normalize_mel(audio):
    # Min is -25, max is 10
    return (audio + 25) / 35


def get_similarity(audio1, audio2):
    audio1 = get_data(audio1[-mschunk:])
    audio2 = get_data(audio2[:mschunk])
    # print(audio1)
    # print(audio2)
    return np.dot(audio1, audio2) / (np.linalg.norm(audio1) * np.linalg.norm(audio2))
    
def compare_two_audio(audio1, audio2):
    # print("Comparing:", audio1, "and", audio2, end=" ")
    audio1 = AudioSegment.from_wav(audio1)
    audio2 = AudioSegment.from_wav(audio2)
    similarity = get_similarity(audio1, audio2)
    # print("Similarity =", similarity)
    return similarity

def combine(part1, part2):
    combined = part1[:-1000] + part1[-1000:].overlay(part2[:1000]) + part2[1000:]
    return combined

def find_most_similar_songs(current_song, mood):
    next_song_lists = np.random.choice(list(map(lambda x: f"extract/{mood}/" + x,os.listdir(f"extract/{mood}"))),size = 100)

    mapper = {}
    start_time = time.time()
    i=0
    for next_song in next_song_lists:
        if current_song != next_song:
            similarity = compare_two_audio(current_song, next_song)
            mapper[next_song] = similarity
        i+=1
        if i % 10 == 0:
            print(i,"/",len(next_song_lists),sep='')

    end_time = time.time()
    print("Wall time:", round(end_time - start_time,2),"seconds")
    print("Current song:", current_song)
    n = 5
    i = 0
    print(f"Top {n} most similar songs:")
    for key, value in sorted(mapper.items(), key=lambda item: item[1], reverse=True)[:n]:
        print(key, value)
        i+=1
        audio1 = AudioSegment.from_wav(current_song)
        audio2 = AudioSegment.from_wav(key)
        combined = combine(audio1, audio2)
        combined.export(f"combined_{i}.wav", format="wav")

find_most_similar_songs("extract/Chill/Good As I Wanted_3.wav", "Chill")
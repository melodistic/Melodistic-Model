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
    normalized_mel = normalize_mel(mels).flatten()
    return normalized_mel

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

def find_most_similar_songs(current_song, mood):
    next_song_lists = np.random.choice(list(map(lambda x: f"extract/{mood}/" + x,os.listdir(f"extract/{mood}"))),size = 100)
    mapper = {}
    for next_song in next_song_lists:
        if current_song != next_song:
            similarity = compare_two_audio(current_song, next_song)
            mapper[next_song] = similarity
    return max(mapper, key=mapper.get)

def postprocessing(audio, time):
    five_second = 5 * 1000
    audio = trim_audio(audio,time)
    audio = match_target_amplitude(audio, -20.0)
    audio = audio.fade_in(five_second).fade_out(five_second)
    return audio
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def trim_audio(audio,time):
    audio = audio[:time * 1000]
    return audio

def combine(part1, part2):
    combined = part1[:-500] + part1[-500:].overlay(part2[:500]) + part2[500:]
    return combined

def combine_all(audio):
    combined = audio[0]
    combined = AudioSegment.from_wav(combined)
    for part in audio[1:]:
        part = AudioSegment.from_wav(part)
        combined = combine(combined, part)
    return combined

def create_list_of_song(mood, n = 1):
    current_song = np.random.choice(list(map(lambda x: f"extract/{mood}/" + x,os.listdir(f"extract/{mood}"))),size = 1)[0]
    song_list = [current_song]
    for _ in range(n):
        next_song = find_most_similar_songs(current_song, mood)
        song_list.append(next_song)
        current_song = next_song
    print(song_list)
    combined = combine_all(song_list)
    combined = postprocessing(combined, 300)
    combined.export("combined.wav", format="wav")

create_list_of_song("Romance")
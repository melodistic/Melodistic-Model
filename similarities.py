import numpy as np
from pydub import AudioSegment
import os
import random
import librosa

mschunk = 500
def get_data(audio):
    samples = audio.get_array_of_samples()
    arr = np.array(samples).astype(np.float32)/32768 # 16 bit 
    arr = librosa.core.resample(arr, audio.frame_rate, 22050, res_type='kaiser_best')
    S = librosa.feature.melspectrogram(arr, sr=22050, n_mels=256)
    mels = np.log(S + 1e-9)
    return mels.flatten()
def normalize(audio):
    # Min is -25, max is 10
    return (audio + 25) / 35

def get_similarity(audio1, audio2):
    audio1 = normalize(get_data(audio1[-mschunk:]))
    audio2 = normalize(get_data(audio2[:mschunk]))
    return np.dot(audio1, audio2)/(np.linalg.norm(audio1)*np.linalg.norm(audio2))

def compare_two_audio(audio1, audio2):
    print("Comparing:", audio1, "and", audio2 ,end = ' ')
    audio1 = AudioSegment.from_wav(audio1)
    audio2 = AudioSegment.from_wav(audio2)
    similarity = get_similarity(audio1, audio2)
    print("Similarity =",similarity)

current_song = "extract/Chill/A New Day_0.wav"
next_song_lists = ["extract/Chill/A New Day_1.wav",
"extract/Chill/Body_4.wav",
"extract/Anxious/A_5.wav",
"extract/Party/Children_3.wav",
"extract/Sad/broken parts_3.wav",
"extract/Romance/All of Me_7.wav",
"extract/Focus/Black Tornado_2.wav"]

for next_song in next_song_lists:
    compare_two_audio(current_song, next_song)



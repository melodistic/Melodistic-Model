from pydub import AudioSegment
import os
import random
import librosa
from spleeter.separator import Separator
import shutil
import pandas as pd

def get_bpm(filepath):
    y, sr = librosa.load(filepath)
    tempo, _ = librosa.beat.beat_track(y,sr)
    return tempo

def detect_leading_silence(sound, chunk_size=10):
    silence_threshold = sound.dBFS * 1.5
    trim_ms = 0 
    assert chunk_size > 0
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def preprocessing(audio):
    start_trim = detect_leading_silence(audio)
    end_trim = detect_leading_silence(audio.reverse())
    duration = len(audio)
    return audio[start_trim:duration-end_trim]

def extracting(audio,filename,mood):
    size = len(audio)
    time_30_sec = 30 * 1000
    audio_list = []
    for i in range(0, size, time_30_sec):
        if i + time_30_sec <= size:
            audio_list.append(audio[i:i+time_30_sec])
    try:
        os.mkdir('extract/'+str(mood))
    except:
        pass
    data = []
    for i in range(len(audio_list)):
        audio_list[i].export("extract/"+str(mood) + "/" + str(filename.split(".")[0]) + "_"+ str(i) + '.wav', format="wav")
        data.append([str(filename.split(".")[0]) + "_"+ str(i) + '.wav',mood])
    return data

def extract_instrumental(separator,audio,name):
    separator.separate_to_file(audio, 'instrumental/')
    os.rename('instrumental/'+name.split('.')[0]+'/accompaniment.wav', 'instrumental/'+name)
    shutil.rmtree('instrumental/'+name.split(".")[0])


if __name__ == '__main__':
    mood_list = os.listdir("song/")
    try:
        os.mkdir('extract')
    except:
        pass
    try:
        os.mkdir("instrumental")
    except:
        pass
    separator = Separator('spleeter:2stems')
    data = []
    for mood in mood_list:
        song_list = os.listdir("song/"+mood)
        for song in song_list:
            extract_instrumental(separator,"song/"+mood+"/"+song,song)
            audio = AudioSegment.from_wav("instrumental/"+song)
            audio = preprocessing(audio)
            data += extracting(audio,song,mood)
            print("Extracting "+song+" done")
    print("Extracting done")
    shutil.rmtree('instrumental')
    df = pd.DataFrame(data,columns=['filename','mood'])
    df.to_csv('data.csv',index=False)
from pydub import AudioSegment
import os
import random
import librosa
from spleeter.separator import Separator
import shutil
import pandas as pd
import gc

def get_bpm(filepath):
    y, sr = librosa.load(filepath)
    tempo, _ = librosa.beat.beat_track(y,sr)
    del y, sr
    gc.collect()
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
    trimmed_sound = audio[start_trim:duration-end_trim]
    del audio
    gc.collect()
    return trimmed_sound

def extracting(audio,filename,mood):
    size = len(audio)
    time_30_sec = 30 * 1000
    audio_list = []
    for i in range(10):
        start = random.randint(0,size-time_30_sec)
        end = start + time_30_sec
        audio_list.append(audio[start:end])
    try:
        os.mkdir('extract/'+str(mood))
    except:
        pass
    data = []
    for i in range(len(audio_list)):
        audio_list[i].export("extract/"+str(mood) + "/" + str(filename.split(".")[0]) + "_"+ str(i) + '.wav', format="wav")
        bpm = get_bpm("extract/"+str(mood) + "/" + str(filename.split(".")[0]) + "_"+ str(i) + '.wav')
        data.append([str(filename.split(".")[0]) + "_"+ str(i) + '.wav', mood, bpm])
    del audio_list
    gc.collect()
    return data

def extract_instrumental(separator,audio,name):
    separator.separate_to_file(audio, 'instrumental/')
    os.rename('instrumental/'+name.split('.')[0]+'/accompaniment.wav', 'instrumental/'+name)
    shutil.rmtree('instrumental/'+name.split(".")[0])
    del audio
    gc.collect()


if __name__ == '__main__':
    mood_list = os.listdir("song/")
    try:
        os.mkdir('extract')
    except:
        pass
    
    separator = Separator('spleeter:2stems')
    data = []
    count = 0
    for mood in mood_list:
        try:
            os.mkdir("instrumental")
        except:
            pass
        song_list = os.listdir("song/"+mood)
        for song in song_list:
            extract_instrumental(separator,"song/"+mood+"/"+song,song)
            audio = AudioSegment.from_wav("instrumental/"+song)
            audio = preprocessing(audio)
            data += extracting(audio,song,mood)
            del audio
            gc.collect()
            count += 1
            print("Extracting "+song+" done"+" ("+str(count)+"/"+str(len(mood_list) * len(song_list))+")")
        shutil.rmtree('instrumental')
    print("Extracting done")
    df = pd.DataFrame(data,columns=['filename','mood','bpm'])
    df.to_csv('data.csv',index=False)

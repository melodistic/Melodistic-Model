from importlib.metadata import files
from multiprocessing import Process
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model,Model
from pydub import AudioSegment
import os
import random
import librosa
from spleeter.separator import Separator
import shutil
import gc
import tensorflow as tf
import numpy as np
import json
def get_bpm(path):
    path = 'extract/' + path + '.wav'
    y, sr = librosa.load(path)
    tempo, _ = librosa.beat.beat_track(y,sr)
    del y, sr
    gc.collect()
    return tempo
def processing(filenames,moods,pred_feats,start,end,pid):
    data = []
    count = 0
    wrong = 0
    for i in range(start,end):
        filename = filenames[i]
        mood = moods[i]
        features = pred_feats[i].flatten().tolist()
        bpm = get_bpm(filename.split(".")[0])
        actual_mood = filename.split("/")[0]
        if mood != actual_mood:
            print(filename + " Wrong prediction: " + mood + ", it should be "+ actual_mood)
            mood = actual_mood
            wrong += 1
        data.append({
            "name":filename,
            "bpm":bpm,
            "mood":mood,
            "features":features})
        count+=1
        print("Process ",pid,str(count)+"/"+str(end-start))
    print("Process ",pid," finished Accuracy: ",str(100*(count-wrong)/count),"%") 
    json.dump(data,open(f"{mood}.json","w"))
if __name__ == "__main__":
    mood_list = os.listdir("spectogram")
    process_list = []
    model_path = 'models/model_v1.h5'
    model = load_model(model_path)

    test_image_generator = ImageDataGenerator(rescale=1./255)
    test_data = test_image_generator.flow_from_directory(
        directory="spectogram",
        class_mode=None,
        target_size=(224,224),
        batch_size=128,shuffle=False)
    
    pred = model.predict(test_data)
    moods = np.argmax(pred, axis=1)
    moods = [list(test_data.class_indices)[x] for x in moods]

    print("Finished predict moods")

    feature_model = Model(model.input,model.layers[-7].output)
    pred_feats = feature_model.predict(test_data)

    print("Finished predict features")

    filenames = test_data.filenames

    print("Start get bpm")
    n = 20
    length = len(filenames)
    each = length//n
    for i in range(n):
        start = i*each
        end = (i+1)*each
        p = Process(target=processing,args=(filenames,moods,pred_feats,start,end,i))
        process_list.append(p)
    for p in process_list:
        p.start()
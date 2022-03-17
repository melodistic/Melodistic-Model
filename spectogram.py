import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import gc

def scale_minmax(X, min=0.0, max=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled

def save_image(data,filename,mood):
    img = scale_minmax(data, 0, 255).astype(np.uint8)
    img = np.flip(img, axis=0) # put low frequencies at the bottom in image
    img = 255-img
    im = Image.fromarray(img)
    im = im.resize((224,224))
    im.save("spectogram/"+ mood +'/'+ filename)
    del img, im
    gc.collect()

def convert_audio_to_mel_spectogram(filename,mood):
    x, sr = librosa.load(filename)
    S = librosa.feature.melspectrogram(x, sr=sr, n_mels=256)
    mels = np.log(S + 1e-9)
    save_image(mels,filename.split("/")[-1].split('.')[0] + '.png',mood)
    del x, sr, S, mels
    gc.collect()
    

if __name__ == '__main__':
    os.makedirs("spectogram",exist_ok=True)
    mood_lists = os.listdir("extract")
    for mood in mood_lists:
        os.makedirs("spectogram/"+mood,exist_ok=True)
        for filename in os.listdir("extract/"+mood):
            convert_audio_to_mel_spectogram("extract/"+mood+"/"+filename,mood)
            print("Done " + filename)
    
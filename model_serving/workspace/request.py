import requests
import os
from get_lyric_song import get_vocal, processing_lyric, get_lyric
import torch
import json
import numpy as np
from miniaudio import decode
from scipy.io import wavfile
from io import BytesIO
import torchaudio
import librosa
from pathlib import Path
from miniaudio import decode, SampleFormat

url = "http://localhost:8080/predictions/lyric_align"

data_dir = "../data/"

metadata = torchaudio.info(data_dir + "sample.wav")
print(metadata)

files = {
    'data' : open(data_dir + "sample.wav", "rb"),
    'script' : open(data_dir + "sample.txt")
}

with open(data_dir + "sample.wav", "rb") as f:
    vocal = f.read()
lyric = get_lyric(data_dir + "sample.txt")
jsons= {
    'data' : vocal,
    #'meta' : metadata,
    #'script' : lyric
}
print(type(vocal))

#audiobyte = Path(data_dir + "sample.wav").read_bytes()
#minivocal = decode(audiobyte, nchannels=1, sample_rate=44100, output_format=SampleFormat.SIGNED32)
#vocal_tensor = torch.FloatTensor(minivocal.samples)
#vocal_tensor /= (1 << (32 - 1))
#print(vocal_tensor)

#wav_content, _ = librosa.load(data_dir + "sample.wav", sr = 44100)
#print(wav_content)
response = requests.post(url, json = json.dumps(jsons))

data = response.content
print(data)
#with open("response.txt", "wb") as response_handler:
#    response_handler.write(data)
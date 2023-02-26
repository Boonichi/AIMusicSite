import requests
import os
from get_lyric_song import get_vocal, processing_lyric, get_lyric
import torch
import json
import numpy as np
from scipy.io import wavfile
from io import BytesIO
import torchaudio
import librosa
from pathlib import Path
from miniaudio import decode, SampleFormat
import soundfile as sf

url = "http://localhost:8080/predictions/lyric_align"

data_dir = "../data/"

metadata = torchaudio.info(data_dir + "sample.wav")
print(metadata)

files = {
    'data' : open(data_dir + "sample.wav", "rb"),
    'script' : open(data_dir + "sample.txt")
}

response = requests.post(url, files = files)
print(response.json())
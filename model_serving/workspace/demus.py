from demucs import pretrained
from demucs.apply import apply_model
from demucs.audio import convert_audio

import os

import torch
import torchaudio
from util import gpu_device

import numpy as np
import librosa

#device = torch.device(gpu_device())

def get_denoiser(device="cpu"):
    # Use a pre-trained model
    separator = pretrained.get_model(name="mdx").models[3]
    separator.to(device)
    separator.eval()
    return separator


def downsample(vocal, original_sr=44100, targ_sr = 16000):
        lowSignal = librosa.resample(vocal, orig_sr=original_sr, target_sr=targ_sr)
        return lowSignal

def run_denoiser(separator, vocal,sample_rate=None,get_vocal_function=None):
    global mix,sr

    if(get_vocal_function!=None):
        mix,sr=get_vocal_function(vocal)
    else:
        mix=vocal
        sr=sample_rate

    mix = downsample(mix)
    
    if((type(mix)==np.ndarray or type(mix)==torch.Tensor)):
        if(type(mix)==np.ndarray):
            mix=torch.from_numpy(mix)
    else:
        if(get_vocal_function == None):
            raise TypeError('get_vocal_function must return numpy.ndarry or torch.Tensor')
        else:
            raise TypeError('vocal must be in numpy.ndarray or torch Tensor type') 

    return mix, sr
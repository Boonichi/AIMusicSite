import torch
import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import soundfile as sf
import librosa
import scipy
import json
import os
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from dataclasses import dataclass
from demucs import pretrained
from demucs.apply import apply_model
from demucs.audio import convert_audio
import requests
from selenium import webdriver
from time import sleep 
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
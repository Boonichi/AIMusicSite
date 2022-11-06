import logging

from librosa import cqt
from librosa.feature import melspectrogram

from util import load_dataset, fcall, save_data

from tqdm import tqdm


@fcall
def preprocess_dataset(args):
    dataset = load_dataset()
    return dataset
import logging

from librosa import cqt
from librosa.feature import melspectrogram

from util import load_dataset, fcall, save_data

from Dataset.SongLoader import SongLoader
from Dataset.LyricsLoader import LyricsLoader

from tqdm import tqdm


@fcall
def preprocess_dataset(args):
    dataset = load_dataset(args["raw_dataset"])
    return dataset

def identify_data_handler(args):
    handler_map = {
        "LyricLoader" : LyricsLoader,
        "SongLoader" : SongLoader
    }
    
    try:
        return handler_map[args["prepare"]["handler"]]
    except KeyError:
        raise NotImplementedError("Unrecognized data handler type {}!".format(args["model"]))
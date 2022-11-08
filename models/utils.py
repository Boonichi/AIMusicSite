import logging
import os

from librosa import cqt
from librosa.feature import melspectrogram

from util import load_dataset, fcall, save_data, ensure_path

from Dataset.SongLoader import SongLoader
from Dataset.LyricsLoader import LyricsLoader
from Dataset.pipeline import SongPipeline

from tqdm import tqdm

import numpy as np


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

def get_model_path(args):
    res_path = os.getcwd() / "storages" 
    ensure_path(res_path)
    return res_path

@fcall
def prepare_input(args):
    pipeline = SongPipeline(args).init_from_model_config()
    data_path = get_model_path(args)

    for ds_type in ["train", "test"]:
        path = data_path / "{}.json".format(ds_type)
        if not os.path.exists(path):
            logging.critical("Expected {} file in path".format(path))
            exit(1)

        data = load_dataset(path)
    
@fcall
def setup_model(args):
    
    return 0
    
@fcall
def load_model_input(args, fold):

    logging.info("Loading preprocessed {} dataset".format(fold))
    path = get_model_path(args)
    X = load_dataset(path / "X_{}.json".format(fold))
    Y = load_dataset(path / "Y_{}.json".format(fold))
    return X, np.array(Y)

@fcall
def train(args):
    model = setup_model(args)
    train_dataset = load_model_input(args, "train")
    test_dataset = load_model_input(args, "test")
    model.fit(train_dataset, test_dataset)

    test_dataset = load_model_input(args, "test")
    model.score(test_dataset)

@fcall
def test(args):
    return 0
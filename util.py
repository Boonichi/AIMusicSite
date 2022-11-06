import sys
import numpy as np
import random
import torch
import logging
import json
import time
from datetime import timedelta
import pickle
import os

from collections import defaultdict

import librosa

def set_random_seed(args):
    if "torch" in sys.modules:
        torch.manual_seed(args["random_seed"])
    np.random.seed(int(args["random_seed"]))
    random.seed(args["random_seed"])

def setup_logging(args):
    
    level = {
        "info" : logging.INFO, 
        "debug" : logging.DEBUG,
        "critical" : logging.CRITICAL
    }
    
    msg_format = '%(asctime)s:%(levelname)s: %(message)s'
    formatter = logging.Formatter(msg_format, datefmt = '%H:%M:%S')
    args = args["logging"]

    file_handler = logging.FileHandler(args["filename"], mode = args["filemode"])
    file_handler.setLevel(level=level[args["level"]])
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    
    logger = logging.getLogger()
    logger.setLevel(level[args["level"]])

def load_raw_dataset(path: str):
    label_path = os.path.join(path, "labels")
    song_path = os.path.join(path, "songs")
    Dataset = defaultdict()

    for l_file in os.listdir(label_path):
        path = os.path.join(label_path, l_file)
        l_content = load_dataset(path)
    
    return l_content


def load_dataset(path: str, raw_state = False):
    
    logging.info("Load dataset {}!".format(path))
    path = str(path)
    
    if raw_state == False:
        if "json" in path:
            with open(path, encoding = "utf-8") as f:
                if ".jsonl" in path:
                    data = [json.loads(line) for line in f]
                elif ".json" in path:
                    data = json.loads(f.read())
        elif "pickle" in path:
            with open(path, "rb") as f:
                data = pickle.load(f)
    elif raw_state == True:
        load_raw_dataset(path)
    else:
        raise NotImplementedError("Don't know how to load a dataset of this type")

    logging.info("Loaded {} records!".format(len(data)))
    return data

def fcall(fun):
    """
    Convenience decorator used to measure the time spent while executing
    the decorated function.
    :param fun:
    :return:
    """
    def wrapper(*args, **kwargs):

        logging.info("[{}] ...".format(fun.__name__))

        start_time = time.perf_counter()
        res = fun(*args, **kwargs)
        end_time = time.perf_counter()
        runtime = end_time - start_time

        logging.info("[{}] Done! {}s\n".format(fun.__name__, timedelta(seconds=runtime)))
        return res

    return wrapper

def dump_dataset(path,data, verbose = True):
    if verbose:
        print("Dump Dataset {}: {}!".format(path, len(data)))
    
    def dump_data():
        if '.json' in path:
            with open(path, 'wb') as f:
                json.dump(data, f)
        elif '.pickle' in path:
            with open(path, 'wb') as f:
                pickle.dump(data, f)
    
    path = str(path)
    try:
        dump_data()
    except FileNotFoundError:
        directory_path = "/".join(path.split("/")[:-1])
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok= True)
            dump_data()

@fcall
def parser_config(path):
    
    return load_dataset(path)

def save_data(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    f.close()
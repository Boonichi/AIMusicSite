import logging
from Dataset.DataLoader import DataLoader
from util import load_dataset, ensure_path
import os
from pathlib import Path
import numpy as np
from tqdm import tqdm
from collections import defaultdict

class SongLoader(DataLoader):
    
    def __init__(self, args, data):
        super().__init__(args, data)
        self.params = self.args["prepare"]["source"]
    
    def prepare(self):
        
        logging.debug("Preparing sources for {} problems..".format(len(self.data)))
        
        skipped = 0
        result = []
        
        for sample in tqdm(self.data):
            
            sample = self.prepare_problem(sample)
            if not sample:
                skipped +=1
            elif len(sample["song"]) > 0:
                result.append(sample)
        self.data = result

        logging.info("{} songs skipped..".format(skipped))
        logging.info("Prepared {} songs".format(len(self.data)))
    
def prepare_problem(self, sample):
    songs = []
    for idx, song in enumerate(sample["songs"]):
        try:
            song = self.prepare_song(song)
            if not song:
                continue
            songs.append(song)
        except Exception as e:
            logging.error("Exception '{}' occurred while parsing solution {}".format(repr(e), str(song["index"])))
        sample["songs"]  = songs

    if len(songs) == 0:
        return None

    return sample
def prepare_song(self, song):
    
    songs = defaultdict()    

    raw = song
    pipeline = [

    ]

    for fun in pipeline:
        song = fun(song)
        if not song:
            return None
    
    songs["raw"] = raw
    songs["preprocessed"] = song

    return songs

            
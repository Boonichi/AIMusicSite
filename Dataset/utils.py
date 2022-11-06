from util import dump_dataset, load_dataset, fcall
from collections import defaultdict
import os
import logging
from tqdm import tqdm

@fcall
def load_raw_dataset(args):
    path = args["raw_dataset"]
    label_path = os.path.join(path, "labels")
    song_path = os.path.join(path, "songs")
    Dataset = list()

    for index,l_file in tqdm(enumerate(os.listdir(label_path))):
        sample = defaultdict()
        name = l_file.split(".")[0]

        l_path = os.path.join(label_path, l_file)
        s_path = os.path.join(song_path, name + ".wav")
        
        l_content = load_dataset(l_path)
        s_content = load_dataset(s_path)
        
        sample['lyrics'] = l_content
        sample['songs'] = {
            "index" : name,
            "song" : s_content
        }
        Dataset.append(sample)
    dump_dataset("./storage/raw_data.pickle", Dataset)
import os
from pathlib import Path

from lyric_align import Lyrics_to_alignment

from demus import *

from result_to_json import *

from get_lyric_song import get_vocal, processing_lyric, get_lyric

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

from util import gpu_device

import ts.model_server 


def main():
    current_dir = Path(os.getcwd())
    data_dir = current_dir / "data"

    mix, sr = get_vocal(os.path.join(data_dir, "sample.wav"))
    
    lyric = get_lyric(os.path.join(data_dir, "sample.txt"))
    lyric, lyric_len = processing_lyric(' '.join(lyric))
    
    #Pretrained
    device = "cpu"
    model = Wav2Vec2ForCTC.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h")
    model.to(device)
    model.eval()

    processor = Wav2Vec2Processor.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h")

    # Sample Data
    lyric_align = Lyrics_to_alignment(model = model, processor=processor, device = device)
    lyric_align.preprocess(mix, sr, lyric)
    word, trellis_length , vocal = lyric_align.predict()
    
    output = convert_to_json_form(word,lyric,lyric_len,converto_time,trellis_length,len(vocal),'output/','result.json')
if __name__ == "__main__":
    main()
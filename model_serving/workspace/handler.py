import torch
import logging
import transformers
import os
import json
from io import BytesIO
import torchvision
from torchaudio.io import _stream_reader
from scipy.io import wavfile
import soundfile as sf
import librosa

from ts.torch_handler.base_handler import BaseHandler
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

from lyric_align import Lyrics_to_alignment

from get_lyric_song import get_vocal, processing_lyric

from result_to_json import convert_to_json_form


logger = logging.getLogger(__name__)
logger.info("Transformers version %s", transformers.__version__)

class ModelHandler(BaseHandler):

    def initialize(self, context):
        """Initialize function loads the model and the tokenizer

        Args:
            context (context): It is a JSON Object containing information
            pertaining to the model artifacts parameters.
        """

        properties = context.system_properties
        self.manifest = context.manifest
        model_dir = properties.get("model_dir")

        logger.info(f'Properties: {properties}')
        logger.info(f'Manifest: {self.manifest}')

        self.device = "cpu"

        model_file = self.manifest['model']['modelFile']
        model_path = os.path.join(model_dir, model_file)
        
        if os.path.isfile(model_path):
            model = Wav2Vec2ForCTC.from_pretrained(model_dir)
            model.to(self.device)
            model.eval()
            logger.info(f'Successfully loaded model from {model_file}')
        else:
            raise RuntimeError('Missing the model file')
        
        processor = Wav2Vec2Processor.from_pretrained(model_dir)
        if processor is not None:
            logger.info('Successfully loaded processor')
        else:
            raise RuntimeError('Missing processor')    
            
        self.lyric_align = Lyrics_to_alignment(model = model, processor= processor, device = self.device)
        if self.lyric_align is not None:
            logger.info("Successfully loaded Lyric Alignment")
        else:
            raise RuntimeError("Lyric Alignment cant be loaded")
            
        self.initialized = True

    def preprocess(self, requests):
        samples = []
        for idx, data in enumerate(requests):
            sample = dict()
            raw_lyric = data.get('script')      
            raw_wav = data.get('data') 

            wav, sr = get_vocal(BytesIO(raw_wav))
            lyric = raw_lyric.decode("utf-8")
            lyric , lyric_len = processing_lyric(lyric)

            #logger.info(wav)
            #logger.info(lyric)
            
            sample["wav"] = wav
            sample["sr"] = sr
            sample["lyric"] = lyric
            sample["lyric_len"] = lyric_len
        
            samples.append(sample)
        logger.info("Data Loaded")
        
        return samples

    def inference(self, inputs):
        result = []
        for sample in inputs:

            output = dict()
            self.lyric_align.preprocess(vocal = sample["wav"], sr = sample["sr"], lyric = sample["lyric"])
            word, trellis_len, vocal = self.lyric_align.predict()
            
            output["word"] = word
            output["trellis_len"] = trellis_len
            output["vocal"] = vocal
            output["lyric"] = sample["lyric"]
            output["lyric_len"] = sample["lyric_len"]
            output["wav_len"] = len(vocal)

            result.append(output)

        logger.info("Prediction Process Done")
        return result

    def postprocess(self, inputs):
        outputs = []
        for sample in inputs:


            output = convert_to_json_form(sample["word"], sample["lyric"], sample["lyric_len"], sample["trellis_len"], sample["wav_len"])
            outputs += output
        
        return outputs
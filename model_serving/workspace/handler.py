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

from ts.torch_handler.base_handler import BaseHandler
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

from lyric_align import Lyrics_to_alignment

from get_lyric_song import get_vocal


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
            raw_script = data.get('script')
            script = raw_script.decode("utf-8")
            
            logger.info(script)

            mix = BytesIO(data['data'])
            
            logger.info(mix)

            sr, wav = get_vocal(mix)

            logger.info(wav)
            

        logger.info("Data Loaded")

        return samples

    def inference(self, vocal, sr, lyric, lyric_len):
        
        word, trellis_length, vocal = self.lyric_align.predict()
        
        logger.info("Prediction Process Done")
        logger.info("Word Prediction: ", word)
        return word, trellis_length, vocal, lyric_len

    def postprocess(self, word, trellis_length, vocal, lyric_len):
        logger.info(word)
        return word

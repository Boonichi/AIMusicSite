import logging

from keras.preprocessing import sequence
import numpy as np

class FeatureParser(object):
    def __init__(self, args, scenario_params, encoder, input_field):
        self.args = args
        self.encoder = encoder
        self.input_type = scenario_params["input"]
        self.input_field = input_field

    def _fit_input(self, input_field):
        raise NotImplementedError()
    
    def filter_incompatible_sample(self, samples):
        return [x for x in samples if self.input_field in x]

class SongParser(FeatureParser):
    def __init__(self, args, scenario_params, encoder, input_field):
        super().__init__(args, scenario_params, encoder, input_field)
        
    def _fit_input(self, input_field):
        return input_field
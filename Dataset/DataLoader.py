from util import load_dataset, dump_dataset, print_defaultdict
from collections import defaultdict
import numpy as np
import logging

class DataLoader(object):
    
    def __init__(self, args, data):
        self.args = args
        self.data = data
    
    def prepare(self):
        raise NotImplementedError()

    

from Dataset.parsers import SongParser

class SongPipeline(object):
    handlers = {
        "SongParser" : SongParser
    }
    def __init__(self, args):
        self.args = args
        self.steps = []
    def init_from_model_config(self):
        features = self.args["features"]
        model_params = self.args["models"][self.args["models"]]
        inputs = model_params["encoders"]["inputs"]
        self.steps = []

        for input_kind in inputs:

        scenario_type   = input_kind["scenario"]
        scenario_params = features["scenarios"][scenario_type]
        encoder_type    = input_kind["encoder"]
        encoder_params  = self.args["encoders"][encoder_type]
        embedding_type  = scenario_params["type"]

        parser   = self.handlers[embedding_type](self.args,
                                                    scenario_params,
                                                    encoder_params,
                                                    input_kind["field"])
        self.steps.append(parser)

        return self
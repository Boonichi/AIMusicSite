from Dataset.DataLoader import DataLoader

class LyricsLoader(DataLoader):
    def __init__(self, args, data):
        super().__init__(args, data)

    def prepare(self):
        return 0
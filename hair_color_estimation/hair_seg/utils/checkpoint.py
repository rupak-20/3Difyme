import os
import pickle

import torch

META_FILE = "meta.pt"


class CheckpointManager:
    def __init__(self, path):
        self.path = path

    def __fullpath(self, name):
        return os.path.join(self.path, name)

    def load(self, name, device):
        filepath = self.__fullpath(name + ".tar")
        checkpoint = torch.load(filepath, map_location=device)

        if not os.path.exists(self.__fullpath(META_FILE)):
            return checkpoint

        with open(self.__fullpath(META_FILE), "rb") as fin:
            meta = pickle.load(fin)

        return {**checkpoint, **meta}

import os
import sys

import numpy as np
import torch
from cv2 import imread

from dataset import ImgTransformer
from evaluate import evaluateOne
from models import MobileHairNet
from utils import CheckpointManager

DIR_PATH = os.path.dirname(__file__)
USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")

SAVE_DIR = "checkpoints"
MODEL_NAME = "default"
IMSIZE = 448
MODE = "run"
CHECKPOINT = "train_16"

def build_model(checkpoint):
    model = MobileHairNet()

    if checkpoint:
        model.load_state_dict(checkpoint["model"])

    # Use appropriate device
    model = model.to(device)

    return model


def run(image, model):
    # img_path = args.image
    model.eval()

    transformer = ImgTransformer(IMSIZE, color_aug=False)
    mask = np.zeros((448, 448, 3), np.uint8)
    img = transformer.load(image, mask)
    return evaluateOne(img, model, absolute=False)


def main(image):

    SAVE_PATH = os.path.join(DIR_PATH, SAVE_DIR, MODEL_NAME)
    print("Saving path:", SAVE_PATH)
    checkpoint_mng = CheckpointManager(SAVE_PATH)

    checkpoint = None
    if CHECKPOINT:
        print("Load checkpoint:", CHECKPOINT)
        checkpoint = checkpoint_mng.load(CHECKPOINT, device)

    model = build_model(checkpoint)

    if MODE == "run":
        return run(image, model)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print('1 additional argument expected, passed', len(sys.argv) - 1)
        print('expected "python main.py image_path"')

    elif len(sys.argv) < 2:
        print('1 additional argument expected, passed', len(sys.argv) - 1)
        print('expected "python main.py image_path"')
    
    else:
        img_path = sys.argv[1]
    
        img = imread(img_path)    
        print(main(img))
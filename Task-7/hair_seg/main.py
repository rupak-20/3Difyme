import argparse
import os

import torch

from dataset import ImgTransformer
from evaluate import evaluateOne
from models import MobileHairNet
from utils import CheckpointManager

DIR_PATH = os.path.dirname(__file__)
USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")


def build_model(checkpoint):
    model = MobileHairNet()

    if checkpoint:
        model.load_state_dict(checkpoint["model"])

    # Use appropriate device
    model = model.to(device)

    return model


def run(args, model):
    img_path = args.image
    model.eval()

    transformer = ImgTransformer(args.imsize, color_aug=False)
    img = transformer.load(img_path, maskpath='mask.jpg')
    return evaluateOne(img, model, absolute=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", choices={"run"}, default="run", help="mode to run the network")
    parser.add_argument("-cp", "--checkpoint")
    parser.add_argument("-im", "--image")
    parser.add_argument("--save_dir", type=str, default="checkpoints", help="folder for models")
    parser.add_argument("--model_name", type=str, default="default", help="model name")
    parser.add_argument("--imsize", type=int, default=448, help="training image size")
    args = parser.parse_args()

    print("args: ", args)

    SAVE_PATH = os.path.join(DIR_PATH, args.save_dir, args.model_name)
    print("Saving path:", SAVE_PATH)
    checkpoint_mng = CheckpointManager(SAVE_PATH)

    checkpoint = None
    if args.checkpoint:
        print("Load checkpoint:", args.checkpoint)
        checkpoint = checkpoint_mng.load(args.checkpoint, device)

    model = build_model(checkpoint)

    if args.mode == "run":
        return run(args, model)


if __name__ == "__main__":
    print(main())

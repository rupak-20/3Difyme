"""
Evaluate
"""

import matplotlib.pyplot as plt
import torch

from utils import create_multi_figure

USE_CUDA = torch.cuda.is_available()
DEVICE = torch.device("cuda" if USE_CUDA else "cpu")


def evaluateOne(img, model, absolute=True):
    img = img[0].to(DEVICE).unsqueeze(0)
    pred = model(img)

    if absolute:
        pred[pred > 0.5] = 1.0
        pred[pred <= 0.5] = 0.0
    else:
        pred[pred < 0.4] = 0
        # pred[pred < .90] = 0

    rows = [img[0], pred[0]]

    return create_multi_figure(rows)


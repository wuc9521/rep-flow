import os
import cv2
from skimage import io
from os.path import isfile, join

TEST_DIR = join(os.path.dirname(__file__), f'../data/test')

imgs = [
    io.imread(join(TEST_DIR, f)) for f in os.listdir(TEST_DIR) if isfile(join(TEST_DIR, f))
]


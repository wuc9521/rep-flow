import os
import cv2
from skimage import io
from os.path import isfile, join

TEST_DIR = join(os.path.dirname(__file__), f'../data/test')

imgs = [
    io.imread(join(TEST_DIR, f)) for f in os.listdir(TEST_DIR) if isfile(join(TEST_DIR, f))
]
imgs = imgs[:10]

grays = []
for i in range(0,10):
    grays.append(cv2.cvtColor(imgs[i], cv2.COLOR_BGR2GRAY))

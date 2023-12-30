import os
import cv2
from skimage import io
from os.path import isfile, join

# 图片初始化
# 增加新的bug链增加参数就行
grays = []
imgs = []
TEST_DIR = []

for i in range(1, 2):
    TEST_DIR.append(join(os.path.dirname(__file__), f'../data/guidance/'+str(i)))
    imgs.append([
        io.imread(join(TEST_DIR[i-1], f)) for f in os.listdir(TEST_DIR[i-1]) if isfile(join(TEST_DIR[i-1], f))
    ])
    grays.append([])
    for j in range(0, len(imgs[i-1])):
        grays[i-1].append(cv2.cvtColor(imgs[i-1][j], cv2.COLOR_BGR2GRAY))

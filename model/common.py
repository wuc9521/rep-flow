import os
import cv2
import json
from skimage import io
from os.path import isfile, join

# 图片初始化
# 增加新的bug链增加参数就行
grays = []
imgs = []
TEST_DIR = []

for i in range(1, 2):
    TEST_DIR.append(join(os.path.dirname(__file__), f'../data/guidance/' + str(i)))
    with open('../data/list/'+str(i)+'.json','r') as f:
        data = json.load(f)
    imgs.append([])
    for item in data:
        imgs[i-1].append(io.imread(join(TEST_DIR[i-1], item['screenshot']+'.png')))
    grays.append([])
    for j in range(0, len(imgs[i-1])):
        grays[i-1].append(cv2.cvtColor(imgs[i-1][j], cv2.COLOR_BGR2GRAY))

from .common import *
from .hist import *
from .ssim import *

# 输入用户图片的路径，和比对图片列表
# image_process 只使用了一个模型，返回result[0]为位置 result[1]为得分
def image_process(image_user_path, image_list):
    image_user = io.imread(image_user_path)
    scores = []
    max_score = 0
    max_similar = 0
    for i in range(len(image_list)):
        score = classify_hist_with_split(image_user, image_list[i])
        if score > max_score:
            max_score = score
            max_similar = i
        scores.append(score)
    if max_score < 0.7:
        return "missing"
    return max_similar, max_score

# image_process_withtwo 是结合了两种模型的处理 返回result[0]为位置 result[1]为得分
def image_process_withtwo(image_user_path, image_list,gray_list):
    image_user = io.imread(image_user_path)
    gray_user = cv2.cvtColor(image_user, cv2.COLOR_BGR2GRAY)
    scores = []
    max_score = 0
    max_similar = 0
    for i in range(len(image_list)):
        score_hist = classify_hist_with_split(image_user, image_list[i])
        (score_ssim, diff) = sk_cpt_ssim(gray_user, gray_list[i], full=True)
        # print(score_hist,' ', end='')
        average_score = (3*score_hist+2*score_ssim)/5
        if average_score > max_score:
            max_score = average_score
            max_similar = i
    # print()
    if max_score < 0.65:
         return "missing"
    return max_similar, max_score

# image_process 返回result[0]为位置 result[1]为得分
def t_image_process(image_user_path):
    result = image_process(image_user_path, imgs[0])
    print("position:", result[0], "score:", result[1])

def t_image_process_withtwo(image_user_path):
    result = image_process_withtwo(image_user_path, imgs[0], grays[0])
    print("position:", result[0], "score:", result[1])


t_image_process(join(TEST_DIR[0], 'screenshot_3.png'))
t_image_process_withtwo(join(TEST_DIR[0], 'screenshot_3.png'))

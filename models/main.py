import cv2
from skimage.metrics import structural_similarity as sk_cpt_ssim


def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def classify_hist_with_split(image1, image2, size=(1000, 2000)):
    # RGB每个通道的直方图相似度
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


# 获得一个用户的实时图片，找出最相似图片返回
def image_process(image_target):
    gray_user =cv2.cvtColor(image_target, cv2.COLOR_BGR2GRAY)
    scores = []
    max_score = 0
    max_similar = 0
    for i in range(0, 10):
        score_hist = classify_hist_with_split(image_target, image_list[i])
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


def test_hist():
    score_list = []
    for i in range(0, 10):
        score_list.append(classify_hist_with_split(image_user,image_list[i]))
    print('三直方图相似度')
    for i in range(0, 10):
        print(score_list[i],end='')
    print()
    for i in range (0,10):
        for j in range (0,10):
            print(classify_hist_with_split(image_list[i],image_list[j]),end='')
        print()

def test_ssim():
    image_user = cv2.imread('../data/image_test/user1.jpg')
    gray_user = cv2.cvtColor(image_user, cv2.COLOR_BGR2GRAY)
    score_list = []
    for i in range(0, 10):
        (score, diff) = sk_cpt_ssim(gray_user, gray_list[i], full=True)
        score_list.append(score)
    print('SSIM相似度')
    for i in range(0, 10):
        print(score_list[i],' ', end='')
    print()
    for i in range(0, 10):
        for j in range(0, 10):
            (score, diff) = sk_cpt_ssim(gray_list[i], gray_list[j], full=True)
            print(score," ",end='')
        print()


image_list =[]
for i in range(1, 11):
    image_list.append(cv2.imread('../data/image_test/test'+str(i)+'.jpg'))

# 使用色彩空间转化函数 cv2.cvtColor( )进行色彩空间的转换
gray_list = []
for i in range(0,10):
    gray_list.append(cv2.cvtColor(image_list[i], cv2.COLOR_BGR2GRAY))

# test_ssim()

for i in range(1, 7):
    image_user = cv2.imread('../data/image_test/user'+str(i)+'.jpg')
    result = image_process(image_user)
    if result == 'missing':
        print(result)
    else:
        print("position :", result[0], " score :", result[1])

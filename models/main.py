import cv2

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
    scores = []
    max_score = 0
    max_similar = 0
    for i in range(0, 10):
        score = classify_hist_with_split(image_target, image_list[i])
        # print(score, end='')
        if score>max_score :
            max_score = score
            max_similar = i
        scores.append(score)
    # print()
    if max_score < 0.7:
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


image_list =[]
for i in range(1, 11):
    image_list.append(cv2.imread('../data/image_test/test'+str(i)+'.jpg'))

for i in range(1, 7):
    image_user = cv2.imread('../data/image_test/user'+str(i)+'.jpg')
    result = image_process(image_user)
    if result == 'missing':
        print(result)
    else:
        print("position :", result[0], " score :", result[1])

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
def image_process(image1):
    scores = []
    max_score = 0
    max_similar = 0
    for i in range(0, 10):
        score = classify_hist_with_split(image_user, image_list[i])
        if score>max_score :

        scores.append(score)


image_list =[]
for i in range(1, 11):
    image_list.append(cv2.imread('../image_test/test'+str(i)+'.jpg'))

image_user = cv2.imread('../image_test/user1.jpg')

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
# sift = cv2.SIFT_create()

# key_list = []
# des_list = []
# for i in range(0,10):
#     key, des= sift.detectAndCompute(image_list[i], None)
#     key_list.append(key)
#     des_list.append(des)
# key_user,des_user=sift.detectAndCompute(image_user, None)
#
# index_params = dict(algorithm=1, trees=5)
# search_params = dict(checks=50)
# flann = cv2.FlannBasedMatcher(index_params, search_params)
#
# matches_list = []
# for i in range(0, 10):
#     matches = flann.knnMatch(des_list[i], des_user, k=2)
#     print(matches.distance)
#     matches_list.append(matches)
# print(matches_list)

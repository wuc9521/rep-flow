import cv2

def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree

def classify_hist_with_split(image1, image2, size=(1000, 2000)):
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    
    sub_data = sub_data / 3
    return sub_data

def image_process(image_target, image_list):
    scores = []
    max_score = 0
    max_similar = 0
    
    for i in range(len(image_list)):
        score = classify_hist_with_split(image_target, image_list[i])
        if score > max_score:
            max_score = score
            max_similar = i
        scores.append(score)
    
    if max_score < 0.7:
        return "missing"
    
    return max_similar, max_score

image_list = []
for i in range(1, 11):
    image_list.append(cv2.imread(f'../data/test/test{i}.jpg'))

def test_hist(image_user_path):
    image_user = cv2.imread(image_user_path)
    score_list = [classify_hist_with_split(image_user, img) for img in image_list]
    print('三直方图相似度')
    for score in score_list:
        print(score)
    
    for i in range(len(image_list)):
        for j in range(len(image_list)):
            print(classify_hist_with_split(image_list[i], image_list[j]))
    
    result = image_process(image_user, image_list)
    print("position:", result[0], "score:", result[1])
    return result[0], result[1]
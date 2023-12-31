from .common import *


from skimage.metrics import structural_similarity as sk_cpt_ssim
def t_ssim(image_user_path):
    image_user = io.imread(image_user_path)
    gray_user = cv2.cvtColor(image_user, cv2.COLOR_BGR2GRAY)
    score_list = []
    for i in range(0, 10):
        (score, diff) = sk_cpt_ssim(gray_user, gray_list[i], full=True)
        score_list.append(score)
    print('SSIM相似度')
    for i in range(0, 10):
        print(score_list[i], ' ', end='')
    print()
    for i in range(0, 10):
        for j in range(0, 10):
            (score, diff) = sk_cpt_ssim(gray_list[i], gray_list[j], full=True)
            print(score, " ", end='')
        print()
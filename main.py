import cv2
import numpy as np
import matplotlib.pyplot as plt
from drawfunc import *
import os
from arguments import *
from edge_detector import EdgeDetector
from path_extractor import PathExtractor
IMG_HEIGHT=500 # fix the image height

DIR= {
    0:"U", 1:"UR", 2:"R", 3:"DR", 4:"D", 5:"DL", 6:"L", 7:"UL"
}

## STEP 1: Read image
print("Type input image path Here: ", end=" ")
img_path = input()
if img_path.split('.')[-1] != 'jpg' and img_path.split('.')[-1] != 'png':
    assert 0, f"only jpg and png avilable, {img_path.split('.')[-1]} is wrong type!"

img = cv2.imread(img_path)
if img is None:
    raise ValueError(f"Failed to read image: {img_path}")


if (img.shape[0] < img.shape[1]):
    img = cv2.resize(img, (IMG_HEIGHT, IMG_HEIGHT * img.shape[0]//img.shape[1]))
else:
    img = cv2.resize(img, (IMG_HEIGHT * img.shape[1]//img.shape[0], IMG_HEIGHT))

## STEP 2: Get Edge
edge_detector = EdgeDetector(img)
edge_img = edge_detector.detect()

img_name = img_path.split('.')[-2].split('/')[-1]
save_path = os.path.join(os.path.split(img_path)[0], img_name)
print(save_path)
if not os.path.isdir(save_path):
    os.mkdir(save_path)

# edge_img = 255 - edge_img
cv2.imwrite(os.path.join(save_path, f'{img_name}_edge.jpg'), edge_img)
plt.imshow(edge_img)



## STEP 3: Get the path that robot arm should move


#2 line_info[[sp1, sp2], d1, d2, ...]
line_info = []

#3 check layer: ckVec
ckVec = np.zeros(edge_img.shape) # 비면 0, 선 시작은 2, 선 중간은 1, 단일픽셀로 지워진 경우 3(길이가 1인 파티클)
line_info = []

pathExtractor = PathExtractor(edge_img)

# STEP2 이미지를 그리기 위한 선의 궤적을 추출한다. 
#1 이미지의 모든 픽셀이 선으로 표현 가능하도록 한다.
progress_num = 0
pathExtractor.erase_noise()
line_clear = pathExtractor.extract()


# STEP3 얻은 데이터를 출력한다. 
#1 최종 이미지 출력
final_img = print_img(ckVec, line_clear, os.path.join(save_path, f"{img_name}_final") ,True)

#2 선 길이 분포표
line_len = []
for i in line_clear:
    if i == 100:
        continue
    line_len.append(len(i) - 1)
    
plt.hist(line_len)

plt.show()


#3 line_clear를 txt 파일로 내보내기
with open(os.path.join(save_path, f"{img_name}_line.txt"), "w") as f:
    for line in line_clear:
        if line == 100:
            continue
        data = str(line[0][0]) + " " + str(line[0][1]) 
        for j in line[1: ]:
            data = data + " " + str(j)
        
        f.write(data)
        f.write("\n")
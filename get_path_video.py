import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Slider
import numpy as np
import cv2
from tqdm import tqdm

# ===========================================
# 설정
# ===========================================

WIDTH = 800
HEIGHT = 600

FPS = 30
STEP_SIZE = 1

VIDEO_NAME = "result.mp4"
# ==========================================================
# 방향 정의
# ==========================================================

DIR = {
    "U": (-STEP_SIZE, 0),
    "D": (STEP_SIZE, 0),
    "L": (0, -STEP_SIZE),
    "R": (0, STEP_SIZE),
    "UR": (-STEP_SIZE, STEP_SIZE),
    "UL": (-STEP_SIZE, -STEP_SIZE), 
    "DR": (STEP_SIZE, STEP_SIZE), 
    "DL": (STEP_SIZE, -STEP_SIZE)
}


# ==========================================================
# 예제 데이터
# [[x, y], v1, v2, ...]
# ==========================================================
paths = []
print("input *_line.txt path: ", end=" ")
file_path = input()
with open(file_path, "r") as f:
    for line in f:
        items = line.strip().split()
        l = [[int(items[0]), int(items[1])]]
        l.extend(items[2:])
        paths.append(l)
# paths = [paths[0]]


# ===========================================
# Video Writer
# ===========================================

writer = cv2.VideoWriter(
    VIDEO_NAME,
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (WIDTH, HEIGHT)
)

img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

# ===========================================
# Draw
# ===========================================

for path in tqdm(paths):

    row, col = path[0]

    for d in path[1:]:

        drow, dcol = DIR[d]

        nrow = row + drow
        ncol = col + dcol

        img[nrow, ncol] = 255

        # 같은 화면을 여러 장 넣으면 재생 속도 조절 가능
        for _ in range(2):
            writer.write(img)

        row = nrow
        col = ncol

# 마지막 화면 1초 유지
for _ in range(FPS):
    writer.write(img)

writer.release()
print("saved:", VIDEO_NAME)
import numpy as np
# 비면 0, 선 시작은 2, 선 중간은 1, 단일픽셀로 지워진 경우 3(길이가 1인 파티클)

PIXEL_UNVISITED      = 0   # 아직 탐색하지 않은 픽셀
PIXEL_PATH           = 1   # 선의 중간 픽셀
PIXEL_STARTPOINT     = 2   # 선의 시작점
PIXEL_NOISE          = 3   # 노이즈(파티클)로 판명된 픽셀
PIXEL_DISCARDED      = 4   # 탐색했지만 의미 없는 픽셀

class PathExtractor():
    def __init__(self, edge_img):
        self.edge_img = edge_img
        self.line_info=[] #2 line_info[[sp1, sp2], d1, d2, ...]
        #3 check layer: ckVec
        self.ckVec = np.zeros_like(edge_img) # 비면 0, 선 시작은 2, 선 중간은 1, 단일픽셀로 지워진 경우 3
    
    def extract(self):
        pass
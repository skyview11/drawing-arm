import numpy as np
from drawfunc import *
# 비면 0, 선 시작은 2, 선 중간은 1, 단일픽셀로 지워진 경우 3(길이가 1인 파티클)



class PathExtractor():
    def __init__(self, edge_img):
        self.edge_img = edge_img
        self.line_info=[] #2 line_info[[sp1, sp2], d1, d2, ...]
        self.ckVec = np.zeros_like(edge_img) # 비면 0, 선 시작은 2, 선 중간은 1, 단일픽셀로 지워진 경우 3
        ## padding
        self.edge_img[0:2] = 0
        self.edge_img[-3:]=0
        self.edge_img[:,0:2]=0
        self.edge_img[:,-3:]=0
        
    def extract(self, noise_threshold=10, n_max_line=10000):
        line_info = []
        for _ in range(n_max_line):
            line, self.ckVec = lining(self.edge_img, self.ckVec) 
            line_info.append(line)
            if np.all(~self.ckVec^self.edge_img): # ckVec은 지난 edge 성분에 대응하는 점에는 어떠한 값을 남기기 때문에 not 연산 수행하고, edge_img에 xor 한 결과가 모든 픽셀에서 1이면 모든 점을 탐색한 것이 됨. 
                break
        
        ## noise threshold 안넘는 길이 전부 삭제
        filtered_lines = []
        for line in line_info:
            if len(line) > noise_threshold + 1:
                filtered_lines.append(line)
        print(f" Total Line number: {len(filtered_lines)}")
        return filtered_lines
    
    def erase_noise(self):
        """주변 8칸이 모두 비어있는 픽셀은 의미없는 노이즈이므로, 분석 대상에서 제외.
        """
        mask = np.array([[0, 0, 0], [0, 255, 0], [0, 0, 0]])
        for row in range(1, self.edge_img.shape[0]-1):
            for col in range(1, self.edge_img.shape[1]-1):
                sub = self.edge_img[row-1:row+2, col-1:col+2]
                if np.array_equal(sub, mask):
                    self.ckVec[row, col] = PIXEL_NOISE

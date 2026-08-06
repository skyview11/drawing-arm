import cv2
import numpy as np
class EdgeDetector:
    def __init__(self, img: np.ndarray):
        self.img = img
        self.edge_img = None
    def detect(self, algo="Canny"):
        if algo=="Canny":
            self.__detect_canny()
        else:
            raise ValueError("Only Canny is available")
        return self.edge_img
    
    def __detect_canny(self, threshold1=None, threshold2=None):
        """return binary edge image of self.img and update self.edge_img. threshold1 and threshold2 must either both be provided or both be None

        Args:
            threshold1 (int, optional): first threshold of canny edge detector. If None, automatically calculate. Defaults to None.
            threshold2 (int, optional): second threshold of canny edge detector. If None, automatically calculate. Defaults to None.
        """
        if (threshold1==None)^(threshold2==None)==1: ## not supported
            raise ValueError("threshold1 and threshold2 must either both be provided or both be None")
        if threshold1==None: ## automatically calculate
            sigma = 0.33
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            v = np.median(gray)
            threshold1 = int(max(0, (1.0 - sigma) * v))
            threshold2 = int(min(255, (1.0 + sigma) * v))
        self.edge_img = cv2.Canny(self.img, threshold1, threshold2)
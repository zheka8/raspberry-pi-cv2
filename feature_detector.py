import cv2
import time

class FeatureDetector:
    
    def __init__(self, res):
        pass
    
    def detect(self, img, frame_count):
        # convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        num_features = 55
        qual_level = 0.01
        min_distance = 10
        
        corners = cv2.goodFeaturesToTrack(gray, num_features, qual_level, min_distance)
        
        self.show(img, corners)
        
    def show(self, img, corners):
        cv2.imshow("Frame", img)
        for i in corners:
            x,y = i.ravel()
            cv2.circle(img, (x,y), radius=3, color=(0,255,0), thickness=-1)
        
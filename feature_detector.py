import cv2
import time

class FeatureDetector:
    
    def __init__(self, res, num_features):
        self.corners = []
        self.orb = cv2.ORB_create(nfeatures=num_features)
    
    def detect(self, img, frame_count):
        # convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # get features
        '''
        num_features = 55
        qual_level = 0.01
        min_distance = 10
        corners = cv2.goodFeaturesToTrack(gray, num_features, qual_level, min_distance)
        '''
        
        # find keypoints and compute descriptors
        kps = self.orb.detect(gray, None)
        kps, des = self.orb.compute(gray, kps)
        
        self.show(img, kps)
        
    def show(self, img, kps):
        cv2.imshow('Frame', img)
        cv2.drawKeypoints(img, kps, img, color=(0,255,0), flags=0)
        
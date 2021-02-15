import cv2
import time
import collections

class FeatureDetector:
    
    def __init__(self, res, num_features=40, maxlen=40):
        self.corners = []
        self.orb = cv2.ORB_create(nfeatures=num_features)
        self.kps = collections.deque(maxlen=maxlen)

    def detect(self, img, frame_count=0):
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
        
        self.kps.extend(kps)
        print(self.kps)

        #self.show(img, kps)
        self.show(img)

    def show(self, img):
        cv2.imshow('Frame', img)
        #cv2.drawKeypoints(img, kps, img, color=(0,255,0), flags=0)
        cv2.drawKeypoints(img, list(self.kps), img, color=(0,255,0), flags=0)


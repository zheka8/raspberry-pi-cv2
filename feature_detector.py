import cv2
import time
import collections

class FeatureDetector:
    
    def __init__(self, res, num_features=40, maxlen=40):
        self.corners = []
        self.orb = cv2.ORB_create(nfeatures=num_features)
        #self.kps = collections.deque(maxlen=maxlen)
        self.kps = []
        self.des = []
        self.imgs = []

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
       
        # store keypoints, descriptors, and images
        self.kps.append(kps)
        self.des.append(des)
        self.imgs.append(img)

    def show(self, img):
        cv2.imshow('Frame', img)
        #cv2.drawKeypoints(img, kps, img, color=(0,255,0), flags=0)
        cv2.drawKeypoints(img, list(self.kps), img, color=(0,255,0), flags=0)

    def match(self):
        ''' perform keypoint matching from the data stored in the detector
        to do: move this method to the feature detector class
        '''

        matched_imgs = []

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # match between successive frames
        for i in range(1, len(self.imgs)):
            des1, des2 = self.des[i-1], self.des[i]
            kps1, kps2 = self.kps[i-1], self.kps[i]
            img1, img2 = self.imgs[i-1], self.imgs[i]

            matches = bf.match(des1, des2)

            # sort in order of distance
            matches = sorted(matches, key = lambda x: x.distance)

            img_out = cv2.drawMatches(img1, kps1, img2, kps2, matches[:40],
                                      None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            matched_imgs.append(img_out)

            return matched_imgs



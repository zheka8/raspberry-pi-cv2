import cv2
import time
import collections

class FeatureDetector:
    
    def __init__(self, res, num_features=40, maxlen=40):
        self.corners = []
        self.orb = cv2.ORB_create(nfeatures=num_features)
        #self.kps = collections.deque(maxlen=maxlen)

        # store previous frame info
        self.kps_prev = []
        self.des_prev = []
        self.img_prev = None

        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def detect_and_match(self, img, frame_count=0):
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
       
        print(f'Frame {frame_count} Num kps found: ', len(kps))

        if self.img_prev is not None: 
            self.match(kps, des, img)

        self.img_prev = img
        self.kps_prev = kps
        self.des_prev = des

        # store keypoints, descriptors, and images
        '''
        self.kps.append(kps)
        self.des.append(des)
        self.imgs.append(img)
        '''

    def show(self, img, kps):
        #cv2.imshow('Frame', img)
        cv2.drawKeypoints(img, kps, img, color=(0,255,0), flags=0)
        #cv2.drawKeypoints(img, list(self.kps), img, color=(0,255,0), flags=0)
        #cv2.imshow('Matches', img)

    def draw_matches(self, matches, kps, img):
        ''' Draw matches on the current img and return it

        What is this Matcher Object?
        The result of matches = bf.match(des1,des2) line is a list of DMatch objects. 
        This DMatch object has following attributes:
          DMatch.distance - Distance between descriptors. The lower, the better it is.
          DMatch.trainIdx - Index of the descriptor in train descriptors
          DMatch.queryIdx - Index of the descriptor in query descriptors
          DMatch.imgIdx - Index of the train image.
        '''
      
        kps_to_draw_t, kps_to_draw_q = [], []
        for m in matches:
            # extract matched keypoint and save it
            kps_to_draw_t.append(kps[m.trainIdx])
            kps_to_draw_q.append(kps[m.queryIdx])

        img_out = cv2.drawKeypoints(img, kps_to_draw_t, img, color=(255, 0, 0), flags=0)
        img_out = cv2.drawKeypoints(img_out, kps_to_draw_q, img_out, color=(0, 0, 255), flags=0)

        return img_out

    def match(self, kps, des, img):
        ''' perform keypoint matching with previous frame
        '''

        matches = self.bf.match(self.des_prev, des)

        # sort in order of distance
        matches = sorted(matches, key = lambda x: x.distance)

        # display matched keypoints on the current image
        img_out = self.draw_matches(matches, kps,  img)

        '''
        img_out = cv2.drawMatches(img1, kps1, img2, kps2, matches[:40],
                                  None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        '''
        
        cv2.imshow('InMatch', img_out)
        key = cv2.waitKey(1) & 0xFF           




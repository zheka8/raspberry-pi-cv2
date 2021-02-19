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
       
        print(f'Frame {frame_count} Num kps found: ', len(kps))

        # store keypoints, descriptors, and images
        self.kps.append(kps)
        self.des.append(des)
        self.imgs.append(img)

        #self.show(img, kps)

        #print('len self.imgs', len(self.imgs))

    def show(self, img, kps):
        #cv2.imshow('Frame', img)
        cv2.drawKeypoints(img, kps, img, color=(0,255,0), flags=0)
        #cv2.drawKeypoints(img, list(self.kps), img, color=(0,255,0), flags=0)
        #cv2.imshow('Matches', img)

    def show_matches(self, matches, kps, img):
        '''
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

    def match(self):
        ''' perform keypoint matching from the data stored in the detector
        '''

        matched_imgs = []

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        #print('inside match, len(self.imgs)', len(self.imgs))

        # match between successive frames
        for i in range(1, len(self.imgs)):
            des1, des2 = self.des[i-1], self.des[i]
            kps1, kps2 = self.kps[i-1], self.kps[i]
            img1, img2 = self.imgs[i-1], self.imgs[i]

            matches = bf.match(des1, des2)

            #print('imgIdx: ', matches[0].imgIdx)

            # sort in order of distance
            matches = sorted(matches, key = lambda x: x.distance)

            # display matched keypoints on the current image
            time.sleep(0.2)
            img_out = self.show_matches(matches, kps2,  img2)

            #print('num matches: ', len(matches))
            #print('i: ', i)
            #print(self.imgs)
            '''
            img_out = cv2.drawMatches(img1, kps1, img2, kps2, matches[:40],
                                      None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            '''
            
            cv2.imshow('InMatch', img_out)
            key = cv2.waitKey(1) & 0xFF           

            matched_imgs.append(img_out)

        return matched_imgs



#!/usr/bin/env python3

import cv2 # OpenCV library
import argparse
from object_detector import ObjectDetector
from feature_detector import FeatureDetector
from camera import Camera
from video_reader import VideoReader

def main():
    # set up argument parser
    parser = argparse.ArgumentParser(description='Object Detection')
    parser.add_argument('-n', '--num_frames', required=True, type=int,
                        help='number of frames to process')
    parser.add_argument('-fps', '--frames_per_second', required=True, type=int,
                        help='frames per second')
    parser.add_argument('-rot', '--rotation', required=True, type=int,
                        help='camera rotation')
    parser.add_argument('-v', '--video', required=False, type=str,
                        help='optional path to pre-recorded video file')

    args = parser.parse_args()

    res = (416, 416)

    # create detector
    #det = ObjectDetector(res, 4)
    det = FeatureDetector(res, num_features=200, maxlen=1000)
   
    # use camera if video file is not provided
    if args.video is None:
        camera = Camera(args.rotation, res, args.frames_per_second)
        camera.run(args.num_frames, det)
    else:
        video_reader = VideoReader(args.video) 
        video_reader.read_and_process(resize_by=0.25, num_frames=args.num_frames, detector=det)

        
    input('type to exit')

if __name__ == '__main__':
    main()

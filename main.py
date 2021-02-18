#!/usr/bin/env python3

from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import argparse
from object_detector import ObjectDetector
from feature_detector import FeatureDetector

def setup_camera(rotation: int, resolution: tuple, FPS: int) -> PiCamera:
    ''' setup the pi camera and return it
    '''
    camera = PiCamera()
    camera.rotation = rotation
    camera.resolution = resolution
    camera.framerate = FPS
    
    return camera

def run_camera(camera: PiCamera, resolution: int, num_frames: int, det: ObjectDetector):
    # Generates a 3D RGB array and stores it in rawCapture
    raw_capture = PiRGBArray(camera, size=resolution)
     
    # Wait a certain number of seconds to allow the camera time to warmup
    time.sleep(0.1)
     
    # Capture frames continuously from the camera
    frame_count = 0
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
         
        # Grab the raw NumPy array representing the image
        image = frame.array
        det.detect(image, frame_count)
        
        #cv2.imshow("Frame", image)
         
        # Wait for keyPress for 1 millisecond
        key = cv2.waitKey(1) & 0xFF
         
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)
         
        # If the `q` key was pressed, break from the loop
        if key == ord("q") or frame_count == num_frames:
            break
        
        frame_count += 1
        
    # After the loop release the cap object 
    #vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 

def main():
    parser = argparse.ArgumentParser(description='Object Detection')
    parser.add_argument('-n', '--num_frames', required=True, type=int,
                        help='number of frames to process')
    parser.add_argument('-fps', '--frames_per_second', required=True, type=int,
                        help='frames per second')
    parser.add_argument('-rot', '--rotation', required=True, type=int,
                        help='camera rotation')

    args = parser.parse_args()

    res = (416, 416)
    FPS = args.frames_per_second
    rotation = args.rotation
    num_frames = args.num_frames
    
    camera = setup_camera(rotation, res, FPS)
    
    #det = ObjectDetector(res, 4)
    det = FeatureDetector(res, num_features=80, maxlen=1000)
    
    run_camera(camera, res, num_frames, det)

    matched_imgs = det.match()

    input('type to exit')

if __name__ == '__main__':
    main()

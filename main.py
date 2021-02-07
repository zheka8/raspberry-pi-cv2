from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy 

def setup_camera(rotation: int, resolution: tuple, FPS: int) -> PiCamera:
    ''' setup the pi camera and return it
    '''
    camera = PiCamera()
    camera.rotation = rotation
    camera.resolution = resolution
    camera.framerate = 10
    
    return camera

def run_camera(camera: PiCamera, resolution: int, num_frames: int):
    # Generates a 3D RGB array and stores it in rawCapture
    raw_capture = PiRGBArray(camera, size=resolution)
     
    # Wait a certain number of seconds to allow the camera time to warmup
    time.sleep(0.1)
     
    # Capture frames continuously from the camera
    frame_count = 0
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
         
        # Grab the raw NumPy array representing the image
        image = frame.array
         
        # Display the frame using OpenCV
        cv2.imshow("Frame", image)
         
        # Wait for keyPress for 1 millisecond
        key = cv2.waitKey(1) & 0xFF
         
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)
         
        # If the `q` key was pressed, break from the loop
        if key == ord("q") or frame_count == num_frames:
            break
        
        frame_count += 1
        
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 

def main():
    camera = setup_camera(90, (640, 480), 10)
    run_camera(camera, (640, 480), 40)

if __name__ == '__main__':
    main()
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library


class Camera:

    def __init__(self, rotation: int, resolution: tuple, FPS: int) -> PiCamera:
        ''' setup the pi camera and return it
        '''
        self.camera = PiCamera()
        self.camera.rotation = rotation
        self.camera.resolution = resolution
        self.camera.framerate = FPS
        
    def run(self, num_frames, detector):
        # Generates a 3D RGB array and stores it in rawCapture
        raw_capture = PiRGBArray(self.camera, size=self.camera.resolution)
         
        # Wait a certain number of seconds to allow the camera time to warmup
        time.sleep(0.1)
         
        # Capture frames continuously from the camera
        frame_count = 0
        for frame in self.camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
             
            # Grab the raw NumPy array representing the image
            image = frame.array
            detector.detect_and_match(image, frame_count)
            
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

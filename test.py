import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray # Generates a 3D RGB array
from main import setup_camera
from object_detector import ObjectDetector
import time

'''
camera = setup_camera(90, (416*2, 416*2), 1)
camera.start_preview()
time.sleep(5)
camera.capture('test.jpg')
camera.stop_preview()
'''

det = ObjectDetector()
img = cv2.imread('horse.jpg')
print(img.shape)
det.detect(img, 0)
cv2.imshow('Image', img)
print(img.shape)
cv2.waitKey(0)
cv2.destroyAllWindows()
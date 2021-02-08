import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray # Generates a 3D RGB array
from main import setup_camera
from object_detector import ObjectDetector
import time

res = (320, 320)

camera = setup_camera(90, res, 1)
camera.start_preview()
time.sleep(5)
camera.capture('test.jpg')
camera.stop_preview()


det = ObjectDetector(res)
img = cv2.imread('test.jpg')
print(img.shape)

t = time.time()
det.detect(img, 0)
print("Inference Time: {0:.2f} sec".format(time.time() - t))

cv2.imshow('Image', img)
print(img.shape)
cv2.waitKey(0)
cv2.destroyAllWindows()
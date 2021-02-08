import cv2
import time

class ObjectDetector:
    
    def __init__(self, resolution):
        self.class_names = self.read_classes('yolov3/coco.names')
        self.net = self.create_net(resolution)
    
    def read_classes(self, filename: str) -> list:
        ''' read class names from a text file
        and return a list
        '''
        
        with open(filename, 'r') as f:
            classes = f.readlines()
            
        return [x.strip('\n') for x in classes]

    def create_net(self, resolution):
        net = cv2.dnn_DetectionModel('yolov3/yolov3-tiny.weights', 'yolov3/yolov3-tiny.cfg')
        
        net.setInputSize(resolution[0], resolution[1]) # TO DO: reshape images?
        net.setInputSwapRB(True) # swap from openCV default to standard RBG
        net.setInputScale(1/255) # convert from 0..255 to 0..1
        net.setInputMean((0,0,0))
        net.setInputCrop(False)
        
        return net


    def detect(self, img, frame_count):
        t = time.time()
        class_ids, confs, bbox = self.net.detect(img, confThreshold=0.5, nmsThreshold=0.5)
        print("Inference Time: {0:.2f} sec".format(time.time() - t))
        
        t = time.time()
        self.show(img, frame_count, class_ids, confs, bbox)
        print("Display Time: {0:.2f} sec".format(time.time() - t))

    def show(self, img, frame_count, class_ids, confs, bbox):
        thickness = 1
        color = (0, 255, 0)

        cv2.imshow('Frame', img)
        if len(class_ids) > 0:
            print('Frame {0}: found something...'.format(frame_count))
            for class_id, conf, box in zip(class_ids.flatten(), confs.flatten(), bbox):
                class_name = self.class_names[class_id].upper()
                label = class_name + ' ' + str(conf)
                print(label)
                
                cv2.rectangle(img, box, color=color, thickness=thickness)
                cv2.putText(img, label, (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 0.5, color, thickness)
        else:
            print('Frame {0}: nothing found'.format(frame_count))
            pass

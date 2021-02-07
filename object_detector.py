import cv2

class ObjectDetector():
    
    def __init__(self):
        self.class_names = self.read_classes('yolov3/coco.names')
        self.net = self.create_net()
    
    def read_classes(self, filename: str) -> list:
        ''' read class names from a text file
        and return a list
        '''
        
        with open(filename, 'r') as f:
            classes = f.readlines()
            
        return [x.strip('\n') for x in classes]

    def create_net(self):
        net = cv2.dnn_DetectionModel('yolov3/yolov3-tiny.weights', 'yolov3/yolov3-tiny.cfg')
        
        net.setInputSize(416, 416) # TO DO: reshape images?
        net.setInputSwapRB(True) # swap from openCV default to standard RBG
        net.setInputScale(1/255) # convert from 0..255 to 0..1
        net.setInputMean((0,0,0))
        net.setInputCrop(False)
        
        return net


    def detect(self, img):
        class_ids, confs, bbox = self.net.detect(img, confThreshold=0.4, nmsThreshold=0.7)
        self.show(img, class_ids, confs, bbox)


    def show(self, img, class_ids, confs, bbox):
        thickness = 2
        color = (0, 255, 0)

        cv2.imshow('Frame', img)
        if len(class_ids) > 0:
            print('Found something...')
            for class_id, conf, box in zip(class_ids.flatten(), confs.flatten(), bbox):
                class_name = classes[class_id].upper()
                print(class_name)
                cv2.rectangle(img, box, color=color, thickness=thickness)
                cv2.putText(img, class_name, (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, color, thickness)
        else:
            print('Nothing found')

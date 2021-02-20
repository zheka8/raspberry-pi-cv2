import cv2

class VideoReader():
    
    def __init__(self, file_path):
        # create a cv2 video capture object
        self.cap = cv2.VideoCapture(file_path)
        self.file_path = file_path

    def read_and_process(self, resize_by=0, num_frames=-1, detector=None):
        ''' read in video and process each frame
        '''

        if not self.cap.isOpened():
            print("Error opening video: ", self.file_path)

        # read frame by frame
        i = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                frame_r = cv2.resize(frame, self.calc_size(frame, resize_by))


                detector.detect_and_match(frame_r, i)
                i += 1
                if num_frames > 0 and i > num_frames:
                    break

    def calc_size(self, frame, scale_factor):
        width = int(frame.shape[1]*scale_factor)
        height = int(frame.shape[0]*scale_factor)

        return (width, height)


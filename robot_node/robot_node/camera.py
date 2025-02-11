import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture("/dev/video0")
        
    def __del__(self):
        if self.video.isOpened():
            self.video.release()
        
    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv2.rectangle(frame, (50,50), (200,200), (0,0,0), 2)
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

def main(args=None):
    rclpy.init(args=args)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

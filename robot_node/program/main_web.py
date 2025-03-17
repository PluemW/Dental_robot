import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2
from flask import Flask, render_template, Response, send_from_directory
import threading

app = Flask(__name__)

# ROS2 Setup
rclpy.init()
bridge = CvBridge()
latest_frame = None  # Store the latest frame

class ROS2CameraSubscriber(Node):
    def __init__(self):
        super().__init__('flask_camera_subscriber')
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
    
    def image_callback(self, msg):
        global latest_frame
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        _, jpeg = cv2.imencode('.jpg', cv_image)
        latest_frame = jpeg.tobytes()

# Start ROS2 in a separate thread
def ros2_thread():
    global ros_node
    ros_node = ROS2CameraSubscriber()
    rclpy.spin(ros_node)

threading.Thread(target=ros2_thread, daemon=True).start()

# Flask Routes
@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory('image', filename)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/controllor')
def controllor():
    return render_template('controllor.html')

@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/test_server')
def test_server():
    return render_template('test_server.html')

# Video Streaming
def generate():
    while True:
        if latest_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n\r\n')

@app.route('/video_cap')
def video_cap():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        ros_node.destroy_node()
        rclpy.shutdown()

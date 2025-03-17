import os
import cv2
from ultralytics import YOLO
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int8, Int8MultiArray
from geometry_msgs.msg import Twist
from rclpy import qos

model = YOLO("robot_node/robot_node/best.pt")

class VideoCamera(Node):
    def __init__(self):
        super().__init__("line_tracker")
        self.pub_direct = self.create_publisher(
            Twist, "/direct_msg", qos.qos_profile_system_default
        )
        self.pub_object = self.create_publisher(
            Int8MultiArray, "/object_msg", qos.qos_profile_system_default
        )

        self.sub_room = self.create_subscription(
            Int8, 
            '/room_msg', 
            self.room_sub, 
            qos.qos_profile_sensor_data
        )
        self.sub_switch = self.create_subscription(
            Bool, 
            '/switch_cam', 
            self.switch_cam_sub, 
            qos.qos_profile_sensor_data
        )
        self.sub_pick = self.create_subscription(
            Bool,
            '/done_pick', 
            self.pickup_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        self.cam_id = 0
        self.cap = cv2.VideoCapture(f'/dev/video{self.cam_id}')
        self.timer = self.create_timer(0.1, self.get_frame)  # 10 FPS
        self.state = 0.0
        self.room_select = 1
        self.linear_x = 0.0  # Base speed
        self.angular_z = 0.0  # Default no turning
        self.pickup = False

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def switch_cam_sub(self, msg):
        new_cam_id = 0 if msg.data else 0
        if new_cam_id != self.cam_id:
            self.cam_id = new_cam_id
            self.cap.release()
            self.cap = cv2.VideoCapture(f'/dev/video{self.cam_id}')
            self.get_logger().info(f"Switched to camera {self.cam_id}")

    def get_frame(self):
        ret, frame = self.cap.read()
        msg_direct = Twist()
        msg_object = Int8MultiArray()
        
        #############################################
        real_height_cm = 16.6 
        camera_angle_deg = 60 
        camera_angle_rad = np.radians(camera_angle_deg) 
        y_levels = [30, 90, 150, 210, 240, 270, 330, 360, 390, 450]
        straight_refs = {270, 360}
        results, points, missing_points, straight_count = {}, [], 0, 0
        area_color = 0
        black_center_x = None
        black_center_y = None
        color_center_x = None
        color_center_y = None
        
        ############## process vision ################
        
        h, w = frame.shape[:2]
        x_center = w // 2
        cm_per_pixel_y = real_height_cm / h
    
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_black = cv2.inRange(hsv, (0, 0, 0), (180, 255, 90))
        mask_red = cv2.inRange(hsv, (0, 75, 0), (20, 255, 255))
        mask_green = cv2.inRange(hsv, (46, 0, 80), (110, 255, 170))
        mask_blue = cv2.inRange(hsv, (80, 90, 100), (115, 255, 210))
        
        if self.room_select == 1:
            mask = mask_black + mask_red
        elif self.room_select == 2:
            mask = mask_black + mask_green
        elif self.room_select == 3:
            mask = mask_black + mask_blue
        else:
            mask = mask_black
            
        ####### Camera drive #######
        if self.cam_id == 2:
            contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_color, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            valid_black = []
            for contour in contours_black:
                for point in contour:
                    y = point[0][1]
                    if 200 <= y <= 480:
                        valid_black.append(contour)
            state_change = sum(cv2.contourArea(cnt) for cnt in valid_black)
            area_color = sum(cv2.contourArea(contour) for contour in contours_color)
            if 30000.0 > area_color >= 12000.0:
                color_center_x, color_center_y = self.get_contour_center(contours_color)
                
            ####### check path #######
            for y in y_levels:
                if y >= h:
                    continue            
                x_coords = np.where(mask[y] == 255)[0]
                median_x = int(np.median(x_coords)) if len(x_coords) > 0 else None
                if median_x is not None:
                    delta_x_pixels = median_x - x_center
                    real_y_cm = (h - y) * cm_per_pixel_y * np.tan(camera_angle_rad)
                    real_x_cm = (delta_x_pixels / w) * real_y_cm                
                    if y in straight_refs:
                        straight_count += 1
                    points.append((y, real_x_cm))
                # else:
                    # if y < 300:
                    #     missing_points += 1  # Increment missing points count
            straight_ratio = straight_count / len(straight_refs)
            self.linear_x, self.angular_z = 0.0, 0.0
            
            ####### condition line #######
            if state_change < 85000000.0: # normal loop
                # if missing_points >= 7 : #### turn angle missing point
                #     x1, x2 = points[-1][1], points[-2][1]
                #     if x2 > x_center + 40:
                #         self.angular_z = -0.4
                #     elif x2 < x_center -40:
                #         self.angular_z = 0.4
                # else: # normal move
                if color_center_y is not None and color_center_y >= 270: # color turn
                    if color_center_x < x_center - 20:
                        self.angular_z = -0.4
                    elif color_center_x > x_center + 20:
                        self.angular_z = 0.4 
                    else: #direct
                        self.linear_x = 0.3 if straight_ratio >= 0.7 else 0.0
                        
                if len(points) >= 3: # normal turn
                    points.sort(reverse=True, key=lambda p: p[0]) 
                    p1, p2, p3 = points[0][1], points[1][1], points[2][1]
                    avg_slope = ((p3 - p2) + (p2 - p1)) / 2
                    if avg_slope > 0.25:
                        self.angular_z += 0.3
                    elif avg_slope < -0.25:
                        self.angular_z -= 0.3 
                    else: #direct
                        self.linear_x = 0.3 if straight_ratio >= 0.7 else 0.0
            else: #stop state
                self.state = 1.0 if not self.pickup else 4.0
        
        ###### Camera pickup ######
        elif self.cam_id == 0:
            if ret and not self.pickup:
                object = model(frame)
                for predict in object: 
                    boxes = predict.boxes
                    for box in boxes:
                        conf = box.conf.item()
                        if conf >= 0.7:
                            self.state = 1.5
                            x1, y1, x2, y2 = map(int, box.xyxy[0]) 
                            x_pos = x1 + x2 / 2
                            y_pos = y1 + y2 / 2
                            if x_center - 10 <= x_pos <= x_center + 10: 
                                if (x2-x1) * (y2-y1) < 1728000.0: # 50% screen 480*720 pixels
                                    self.linear_x = 0.2
                                else:
                                    self.linear_x = 0.0
                                    self.angular_z = 0.0
                                    self.state = 2
                                    msg_object.data = [x_pos, y_pos]
                            else:
                                self.state = 1
                                self.angular_z = -0.2 if x_center - 10 <= x_pos else 0.2
            if ret and self.pickup:
                mask_gray = cv2.inRange(hsv, (0, 0, 0), (180, 255, 90))
                contour_gray,_ = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                mark_x, mark_y = self.get_contour_center(contour_gray)
                msg_object.data = [mark_x, mark_y]

        # control_text = f"Linear X: {self.linear_x:.2f}, Angular Z: {self.angular_z:.2f}"
        # cv2.putText(frame, control_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if ret:
            cv2.imshow("Real-World Positioning", frame)
            cv2.waitKey(1)

        ##############################################
        msg_direct.linear.y = self.state
        msg_direct.linear.x = self.linear_x
        msg_direct.angular.z = self.angular_z
        
        self.pub_direct.publish(msg_direct) 
        self.pub_object.publish(msg_object)
        # _, jpeg = cv2.imencode('.jpg', frame)
        # return jpeg.tobytes()
        
    def get_contour_center(self, contours):
        if not contours:
            return None, None
        max_contour = max(contours, key=cv2.contourArea)  # Get the largest contour
        M = cv2.moments(max_contour)
        return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) if M["m00"] != 0 else (None, None)

    def room_sub(self, msg):
        self.room_select = 1
        # self.room_select = msg.data
    
    def pickup_sub(self, msg):
        if msg.data:
            self.pickup = msg.data
        
    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = VideoCamera()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy import qos, parameter
import numpy as np

node_name = 'gripper_node_msg'

class Gripper(Node):
    def __init__(self):
        super().__init__(node_name)        
        self.pub_gripper_step = self.create_publisher(
            Twist, "/step_gripper", qos_profile=qos.qos_profile_system_default
        )
        
        self.sub_gripper_abs = self.create_subscription(
            Twist, 
            '/abs_gripper', 
            self.abs_gripper_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        self.sub_gripper_abs

        self.sent_timer = self.create_timer(0.05, self.timer_callback)
        # self.declare_parameters
        self.step_theta_1 = 0.0
        self.step_theta_2 = 0.0
        self.roll = 90.0
        self.pick = 90.0
        self.rpm = 150.0
        
    def timer_callback(self):
        msg_abs_grip = Twist()
        msg_abs_grip.linear.x = self.step_theta_1
        msg_abs_grip.linear.z = self.step_theta_2
        msg_abs_grip.angular.y = self.roll
        msg_abs_grip.angular.z = self.pick
        
        self.pub_gripper_step.publish(msg_abs_grip)
    
    def abs_gripper_sub(self, msg):
        grip_length = 0.125
        x = msg.linear.x - grip_length
        z = msg.linear.z
        angles = self.inverse_kinematics_2dof(x, z)
        if angles is not None:
            self.step_theta_1, self.step_theta_2 = angles
    
    def inverse_kinematics_2dof(self, x, z, l1=1.0, l2=1.0):
        d = np.sqrt(x**2 + z**2)        
        if d > (l1 + l2) or d < abs(l1 - l2):
            return None
        cos_theta2 = (x**2 + z**2 - l1**2 - l2**2) / (2 * l1 * l2)
        theta2 = np.arccos(np.clip(cos_theta2, -1.0, 1.0))
        k1 = l1 + l2 * np.cos(theta2)
        k2 = l2 * np.sin(theta2)
        theta1 = np.arctan2(z, x) - np.arctan2(k2, k1)
        theta1, theta2 = self.theta_to_step(theta1, theta2)
        return theta1, theta2

    def theta_to_step(self, theta_1, theta_2):
        step = 13.25 * self.rpm # cpr 1990.0
        theta_1 = theta_1 * step / 360
        theta_2 = theta_2 * step / 360
        return theta_1, theta_2

def main(args=None):
    rclpy.init(args=args)
    node = Gripper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

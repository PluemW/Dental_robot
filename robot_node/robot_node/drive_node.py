import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8MultiArray
from geometry_msgs.msg import Twist
from rclpy import qos

node_name = 'drive_node_msg'

class Drive(Node):
    def __init__(self):
        super().__init__(node_name)
        self.pub_cmd_vel = self.create_publisher(
            Twist, "/cmd_vel", qos.qos_profile_system_default
        )
        self.sub_cmd_vel = self.create_subscription(
            Int8MultiArray, 
            '/cmd_vel_sub', 
            self.cmd_vel_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        
        self.timer = self.create_timer(0.05, self.timer_callback)
        self.current_linear_x = 0.0
        self.current_angular_z = 0.0
        self.target_linear_x = 0.0
        self.target_angular_z = 0.0
        self.max_acceleration = 0.05
        self.max_turn_acceleration = 0.1

    def update_velocity(self, current, target, max_step):
        if abs(target - current) < max_step:
            return target
        return current + max_step * ((target - current) / abs(target - current))

    def timer_callback(self):
        msg_cmd_vel = Twist()
        self.current_linear_x = self.update_velocity(self.current_linear_x, self.target_linear_x, self.max_acceleration)
        self.current_angular_z = self.update_velocity(self.current_angular_z, self.target_angular_z, self.max_turn_acceleration)
        msg_cmd_vel.linear.x = self.current_linear_x
        msg_cmd_vel.angular.z = self.current_angular_z
        self.pub_cmd_vel.publish(msg_cmd_vel)

    def cmd_vel_sub(self, msg):
        if len(msg.data) >= 2:
            self.target_linear_x = float(msg.data[0])
            self.target_angular_z = float(msg.data[1])

def main(args=None):
    rclpy.init(args=args)
    node = Drive()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

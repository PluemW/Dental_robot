import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int8MultiArray
from rclpy import qos, parameter

node_name = 'gripper_node_msg'

class Gripper(Node):
    def __init__(self):
        super().__init__(node_name)
        self.pub_gripper_step = self.create_publisher(
            Bool, "/pub_step_gripper", qos_profile=qos.qos_profile_system_default
        )
        
        self.pub_gripper_abs = self.create_publisher(
            Bool, "/pub_abs_gripper", qos_profile=qos.qos_profile_system_default
        )
        
        self.sub_gripper_step = self.create_subscription(
            Bool, 
            '/sub_step_gripper', 
            self.step_gripper_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        self.sub_gripper_step
        
        self.sub_gripper_abs = self.create_subscription(
            Int8MultiArray, 
            '/sub_abs_gripper', 
            self.abs_gripper_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        self.sub_gripper_abs

        self.sent_timer = self.create_timer(0.05, self.timer_callback)
        self.declare_parameters
    
    def timer_callback(self):
        return
            
    def step_gripper_sub(self, msg):
        return
    
    def abs_gripper_sub(self, msg):
        return

def main(args=None):
    rclpy.init(args=args)
    node = Gripper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

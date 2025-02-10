import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int8
from rclpy import qos, parameter

node_name = 'State_node'

class State(Node):
    def __init__(self):
        super().__init__(node_name)
        self.pub_cmd_vel = self.create_publisher(
            Int8, "/cmd_vel", qos_profile=qos.qos_profile_system_default
        )

        self.sent_timer = self.create_timer(0.05, self.timer_callback)
        self.declare_parameters
    
    def timer_callback(self):
        return
            
    def cmd_vel_sub(self, msg):
        return

def main(args=None):
    rclpy.init(args=args)
    node = State()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

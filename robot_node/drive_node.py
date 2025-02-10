import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8MultiArray, Int8, String
from geometry_msgs.msg import Twist
from rclpy import qos, parameter

node_name = 'drive_node_msg'

class Drive(Node):
    def __init__(self):
        super().__init__(node_name)
        self.pub_cmd_vel = self.create_publisher(
            Twist, "/cmd_vel", qos_profile=qos.qos_profile_system_default
        )
        self.pub_state = self.create_publisher(
            String, "/state_doing", qos_profile=qos.qos_profile_system_default
        )
        
        self.sub_room = self.create_subscription(
            Int8, 
            '/room_msg', 
            self.room_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        self.sub_room
        
        self.sub_cmd_vel = self.create_subscription(
            Int8MultiArray, 
            '/cmd_vel_sub', 
            self.cmd_vel_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        self.sub_cmd_vel

        self.sent_timer = self.create_timer(0.05, self.timer_callback)
        self.declare_parameters
        
        # Parameters
        self.state_room = "-1"
    
    def timer_callback(self):
        state = String()
        state.data = self.state_room
        self.pub_state.publish(state)
            
    def room_sub(self, msg):
        self.state_room = str(msg.data)
        return  self.get_logger().info(f'room: {msg.data}')
    
    def cmd_vel_sub(self, msg):
        return

def main(args=None):
    rclpy.init(args=args)
    node = Drive()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

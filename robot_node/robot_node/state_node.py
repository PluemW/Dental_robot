import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int8, Int8MultiArray
from geometry_msgs.msg import Twist
from rclpy import qos, parameter

node_name = 'State_node'

class State(Node):
    def __init__(self):
        super().__init__(node_name)
        self.pub_cmd_vel = self.create_publisher(
            Twist, "/cmd_vel", qos_profile=qos.qos_profile_system_default
        )
        self.pub_abs_gripper = self.create_publisher(
            Twist, "/abs_gripper", qos_profile=qos.qos_profile_system_default
        )
        self.pub_switch_cam = self.create_publisher(
            Bool, "/switch_cam", qos_profile=qos.qos_profile_system_default
        )
        
        self.sub_direct = self.create_subscription(
            Twist,
            '/direct_msg', 
            self.direct_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        self.sub_object = self.create_subscription(
            Int8MultiArray,
            '/object_msg', 
            self.object_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )
        self.sub_pick = self.create_subscription(
            Bool,
            '/done_pick', 
            self.pickup_sub, 
            qos_profile=qos.qos_profile_sensor_data
        )

        self.sent_timer = self.create_timer(0.05, self.timer_callback)
        # self.declare_parameters
        self.state = 0
        self.receive = True
        self.stand_by = False
        self.drive_linear_x = 0.0
        self.drive_angular_z = 0.0
        self.grip_linear_x = 0.0   # set position distance
        self.grip_linear_z = 0.0
        self.grip_angular_y = 0.0
        self.grip_angular_z = 0.0
        self.switch = False
    
    def timer_callback(self):
        msg_cmd = Twist()
        msg_grip = Twist()
        msg_switch = Bool()
        
        ########## state ###########
        if self.state == 1: # tray turning state
            self.receive = False
            self.switch = True
            self.drive_angular_z = 0.3
        # if self.state == 2: # pick up state

        #####################
        if self.state == 2.5 and not self.stand_by: # stand-by delivery
            self.drive_angular_z = -0.3
        if self.state == 2.5 and self.stand_by:
            self.drive_linear_x = 0.3
            self.drive_angular_z = 0.0
        
        if self.state == 3:
            self.receive = True
            
        if self.state == 4:
            self.receive = False
            self.switch = True
        
        
        ############################
        
        msg_cmd.linear.x = self.drive_linear_x
        msg_cmd.angular.z = self.drive_angular_z
        # pixel cm
        msg_grip.linear.x = self.grip_linear_x
        msg_grip.linear.z = self.grip_linear_z
        msg_grip.angular.y = self.grip_angular_y
        msg_grip.angular.z = self.grip_angular_z
        
        msg_switch.data = self.switch
        
        ############################
        
        self.pub_cmd_vel.publish(msg_cmd)
        self.pub_abs_gripper.publish(msg_grip)
        self.pub_switch_cam.publish(msg_switch)
            
    def direct_sub(self, msg):
        if self.receive: ### move
            self.drive_linear_x = msg.linear.x
            self.drive_angular_z = msg.angular.z
            if self.state == 0 or self.state == 3:
                self.state = msg.linear.y

        if self.switch and not self.stand_by: ### pickup
            self.state = msg.linear.y
            if self.state == 1.5:
                self.drive_linear_x = msg.linear.x
                self.drive_angular_z = msg.angular.z

        if self.state == 2.5: ### stand-by
            if msg.linear.z == 1:
                self.stand_by = True
            if msg.linear.z == 2:
                self.state = 3
        
        if self.switch and self.stand_by: ### dropout
            return        
            
    def object_sub(self, msg):
        # grip_y = msg.data[0] # command move for error
        # grip_z = msg.data[1]
        return
        
    def pickup_sub(self, msg):
        if msg.data and self.state == 2:
            # collected tray position
            self.grip_linear_x = 0.0
            self.grip_linear_z = 0.0
            self.grip_angular_y = 0.0
            self.grip_angular_z = 0.0
            ##########################
            
            self.switch = False
            self.state = 2.5

def main(args=None):
    rclpy.init(args=args)
    node = State()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

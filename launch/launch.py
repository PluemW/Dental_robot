import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

package_name = 'robot_node'

def generate_launch_description():
    package_path = get_package_share_directory(package_name)
    executable_path = PathJoinSubstitution(
        [FindPackageShare(package_name), "program", "main_web.py"]
    )
    
    config_file_path = PathJoinSubstitution(
        [FindPackageShare(package_name), "config_params", "params.yaml"]
    )
    
    rosbridge_server_launch_path = PathJoinSubstitution(
        [FindPackageShare("rosbridge_server"), "launch", "rosbridge_websocket_launch.xml"]
    )

    return LaunchDescription([
        Node(
            package=package_name,
            executable='drive_node',
            name='drive_node',
            output='screen',
            parameters=[config_file_path]
        ),
        Node(
            package=package_name,
            executable='gripper_node',
            name='gripper_node',
            output='screen',
            parameters=[config_file_path]
        ),
        Node(
            package="rosbridge_server",
            executable="rosbridge_websocket",
            name="rosbridge_websocket",
            output="screen",
            parameters=[{"port": 9090}],
        ),
        ExecuteProcess(
            cmd=['python3', executable_path],
            output='screen',
        ),
    ])
    
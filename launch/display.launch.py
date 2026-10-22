"""RViz view of the nacelle with joint sliders.

ros2 launch windturbine_description display.launch.py [urdf:=/abs/path/to/scenario.urdf]
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def nodes(context):
    share = get_package_share_directory("windturbine_description")
    urdf = LaunchConfiguration("urdf").perform(context) or os.path.join(share, "urdf", "windturbine.urdf")
    use_gui = LaunchConfiguration("gui").perform(context).lower() in ("true", "1", "yes")

    with open(urdf) as f:
        description = f.read()
        
    result = [
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": description}]),
        Node(package="rviz2", executable="rviz2", arguments=["-d", os.path.join(share, "rviz", "nacelle.rviz")]),
    ]
    
    if use_gui:
        result.insert(1, Node(package="joint_state_publisher_gui", executable="joint_state_publisher_gui"))
    return result


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("urdf", default_value="", description="URDF to show (default: healthy)"),
        DeclareLaunchArgument("gui", default_value="true",
                              description="Start joint_state_publisher_gui (set false when another node publishes /joint_states)"),
        OpaqueFunction(function=nodes),
    ])

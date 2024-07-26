from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan',
            name='depthimage_to_laserscan',
            namespace='',
            remappings=[
                ('image', '/camera/aligned_depth_to_color/image_raw'),
                ('camera_info', '/camera/color/camera_info')
            ],
            parameters=[
                {'scan_height': 1},
                {'scan_time': 0.033},
                {'range_min': 0.45},
                {'range_max': 10.0},
                {'output_frame_id': 'camera_depth_frame'}
            ]
        )
    ])


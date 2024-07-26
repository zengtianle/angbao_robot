import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    # =============================1.定位到包的地址=============================================================
    angbao_navigation2_dir = get_package_share_directory('angbao_navigation2')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # =============================2.声明参数，获取配置文件路径===================================================
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')  # 在真实机器人环境中使用系统时间
    #use_sim_time = LaunchConfiguration('use_sim_time', default='true')  # 在真实机器人环境中使用系统时间
    #map_yaml_path = LaunchConfiguration('map', default='/home/nvidia/nav2_ws/src/angbao_navigation2/maps/507map.yaml') 
    map_yaml_path = LaunchConfiguration('map',default=os.path.join(angbao_navigation2_dir,'maps','507map.yaml'))
    nav2_param_path = LaunchConfiguration('params_file', default=os.path.join(angbao_navigation2_dir, 'param', 'angbao_params.yaml'))
    rviz_config_dir = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')


    # =============================3.声明参数，获取配置文件路径===================================================
    return LaunchDescription([
        # Declare launch arguments
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use simulation (Gazebo) time'),
        DeclareLaunchArgument('map', default_value='/home/nvidia/nav2_ws/src/angbao_navigation2/maps/507map.yaml', 		description='Full path to the map file to load'),

      

        # Start Navigation2 bringup launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_bringup_dir, '/launch', '/bringup_launch.py']),
            launch_arguments={
                'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_param_path,
            }.items(),
        ),

        # Start RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        )
    ])


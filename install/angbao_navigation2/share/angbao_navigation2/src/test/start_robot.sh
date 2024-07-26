#!/bin/bash

# 打开第一个终端并执行命令
gnome-terminal -- bash -c "docker start angbao_robot"

gnome-terminal -- bash -c "docker exec -it angbao_robot /bin/bash -c 'source devel/setup.bash && roslaunch obrobot_driver driver.launch'"

# 等待一段时间以确保第一个命令已经开始执行
sleep 5

# 打开第二个终端并执行命令
gnome-terminal -- bash -c "docker exec -it angbao_robot /bin/bash -c 'source devel/setup.bash && roslaunch ydlidar lidar.launch'"

# 等待一段时间以确保第二个命令已经开始执行
sleep 5

# 打开第三个终端并执行命令
gnome-terminal -- bash -c "docker exec -it angbao_robot /bin/bash -c 'source devel/setup.bash && roslaunch obrobot_description obrobot_description.launch'"

# 等待一段时间以确保第三个命令已经开始执行
sleep 2

# 打开第四个终端并执行命令
gnome-terminal -- bash -c "source /opt/ros/foxy/setup.bash && ros2 run ros1_bridge dynamic_bridge"

# 等待一段时间以确保第四个命令已经开始执行
sleep 2

# 打开第五个终端并执行命令
gnome-terminal -- bash -c "source /opt/ros/foxy/setup.bash && ros2 run teleop_twist_keyboard teleop_twist_keyboard"

# 等待一段时间以确保第五个命令已经开始执行
#sleep 2

#打开第六个终端并执行命令
gnome-terminal -- bash -c "source /opt/ros/foxy/setup.bash && cd /home/nvidia/nav2_ws/ && source install/setup.bash && ros2 launch angbao_navigation2 navigation.launch.py"

sleep 2
gnome-terminal -- bash -c "source /opt/ros/foxy/setup.bash && cd /home/nvidia/work/ros2_ws/ && source install/setup.bash && ros2 launch realsense2_camera rs_launch.py"


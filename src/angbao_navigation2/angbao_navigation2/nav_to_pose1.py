
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

import rclpy
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import time

from action_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
from lifecycle_msgs.srv import GetState
from nav2_msgs.action import  NavigateToPose

import rclpy

from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile
def main():
    rclpy.init()

    # 创建 NavigateToPose 动作客户端
#   这一行一放出来就报错
    nav_to_pose_client = ActionClient(rclpy.create_node('basic_navigator'), NavigateToPose, '/navigate_to_pose')


    # 等待 NavigateToPose 动作服务器
    nav_to_pose_client.wait_for_server()

    clock = rclpy.clock.Clock()  # 创建 Clock 对象

    # 设置目标点坐标
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = clock.now().to_msg()  # 使用 clock.now() 获取时间戳
    
    goal_pose.pose.position.x = 1.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 1.0

#    print(goal_pose)
#    print(goal_pose.header.stamp)


    # 发送目标点
    goal_msg = NavigateToPose.Goal()
    goal_msg.pose = goal_pose

    print(goal_msg)

    send_goal_future = nav_to_pose_client.send_goal_async(goal_msg)

    # 等待目标发送完成（但不等待目标完成）
#    send_goal_future.wait_for_result()

    print("Goal sent!")

    rclpy.shutdown()

if __name__ == '__main__':
    main()

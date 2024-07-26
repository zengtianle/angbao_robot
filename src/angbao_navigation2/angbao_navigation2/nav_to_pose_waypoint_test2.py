#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import math
import functools


from action_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
from lifecycle_msgs.srv import GetState
from nav2_msgs.action import NavigateToPose

import rclpy
from rclpy.duration import Duration

from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile

from std_msgs.msg import String


class BasicNavigator(Node):
    def __init__(self):
        super().__init__(node_name='basic_navigator')
        self.initial_pose = Pose()
        self.goal_handle = None
        self.result_future = None
        self.feedback = None
        self.status = None

        amcl_pose_qos = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=1)

        self.initial_pose_received = False
        # self.nav_through_poses_client = ActionClient(self,
        #                                              NavigateThroughPoses,
        #                                              'navigate_through_poses')
        self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.model_pose_sub = self.create_subscription(PoseWithCovarianceStamped,
                                                       'amcl_pose',
                                                       self._amclPoseCallback,
                                                       amcl_pose_qos)
        self.initial_pose_pub = self.create_publisher(PoseWithCovarianceStamped,
                                                      'initialpose',
                                                      10)

    def setInitialPose(self, initial_pose):
        self.initial_pose_received = False
        self.initial_pose = initial_pose
        self._setInitialPose()

    def goToPose(self, pose):
        # Sends a `NavToPose` action request and waits for completion
        self.debug("Waiting for 'NavigateToPose' action server")
        while not self.nav_to_pose_client.wait_for_server(timeout_sec=1.0):
            self.info("'NavigateToPose' action server not available, waiting...")

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose

        self.info('Navigating to goal: ' + str(pose.pose.position.x) + ' ' +
                      str(pose.pose.position.y) + '...')
        send_goal_future = self.nav_to_pose_client.send_goal_async(goal_msg,
                                                                   self._feedbackCallback)
        rclpy.spin_until_future_complete(self, send_goal_future)
        self.goal_handle = send_goal_future.result()

        if not self.goal_handle.accepted:
            self.error('Goal to ' + str(pose.pose.position.x) + ' ' +
                           str(pose.pose.position.y) + ' was rejected!')
            return False

        self.result_future = self.goal_handle.get_result_async()
        return True

    def cancelNav(self):
        self.info('Canceling current goal.')
        if self.result_future:
            future = self.goal_handle.cancel_goal_async()
            rclpy.spin_until_future_complete(self, future)
        return

    def isNavComplete(self):
        if not self.result_future:
            # task was cancelled or completed
            return True
        rclpy.spin_until_future_complete(self, self.result_future, timeout_sec=0.10)
        if self.result_future.result():
            self.status = self.result_future.result().status
            if self.status != GoalStatus.STATUS_SUCCEEDED:
                self.info('Goal with failed with status code: {0}'.format(self.status))
                return True
        else:
            # Timed out, still processing, not complete yet
            return False

        self.info('Goal succeeded!')
        return True

    def getFeedback(self):
        return self.feedback

    def getResult(self):
        return self.status

    def waitUntilNav2Active(self):
        self._waitForNodeToActivate('amcl')
        self._waitForInitialPose()
        self._waitForNodeToActivate('bt_navigator')
        self.info('Nav2 is ready for use!')
        return

    def _waitForNodeToActivate(self, node_name):
        # Waits for the node within the tester namespace to become active
        self.debug('Waiting for ' + node_name + ' to become active..')
        node_service = node_name + '/get_state'
        state_client = self.create_client(GetState, node_service)
        while not state_client.wait_for_service(timeout_sec=1.0):
            self.info(node_service + ' service not available, waiting...')

        req = GetState.Request()
        state = 'unknown'
        while (state != 'active'):
            self.debug('Getting ' + node_name + ' state...')
            future = state_client.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            if future.result() is not None:
                state = future.result().current_state.label
                self.debug('Result of get_state: %s' % state)
            time.sleep(2)
        return

    def _waitForInitialPose(self):
        while not self.initial_pose_received:
            self.info('Setting initial pose')
            self._setInitialPose()
            self.info('Waiting for amcl_pose to be received')
            rclpy.spin_once(self, timeout_sec=1)
        return

    def _amclPoseCallback(self, msg):
        self.initial_pose_received = True
        return

    def _feedbackCallback(self, msg):
        self.feedback = msg.feedback
        return

    def _setInitialPose(self):
        msg = PoseWithCovarianceStamped()
        msg.pose.pose = self.initial_pose
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        self.info('Publishing Initial Pose')
        self.initial_pose_pub.publish(msg)
        return

    def info(self, msg):
        self.get_logger().info(msg)
        return

    def warn(self, msg):
        self.get_logger().warn(msg)
        return

    def error(self, msg):
        self.get_logger().error(msg)
        return

    def debug(self, msg):
        self.get_logger().debug(msg)
        return

def my_callback(msg: String,navigator: BasicNavigator):
    global new_goal_pose
    #new_goal_pose = None
    navigator.info('进入回调函数，准备接收消息')
    if msg.data == "向左转":
        navigator.info('向左转')
        #current_pose = navigator.getRobotPose()
        #current_x = current_pose.pose.position.x
        #current_y = current_pose.pose.position.y
        #current_w = current_pose.pose.orientation.w
        
        current_pose = Pose()
        current_x = 5.0
        current_y = 5.0
        current_w = 5.0

        new_x = current_x
        new_y = current_y
        new_w = math.cos(math.pi / 4)  # 原地左转90度

        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = new_x
        goal_pose.pose.position.y = new_y
        goal_pose.pose.orientation.w = new_w

    if msg.data == "向右转":
        navigator.info('向右转')
        #current_pose = navigator.getRobotPose()
        #current_x = current_pose.pose.position.x
        #current_y = current_pose.pose.position.y
        #current_w = current_pose.pose.orientation.w
        
        current_pose = Pose()
        current_x = 5.0
        current_y = 5.0
        current_w = 5.0

        new_x = current_x
        new_y = current_y
        new_w = math.cos(-math.pi / 4)  # 原地右转90度

        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = new_x
        goal_pose.pose.position.y = new_y
        goal_pose.pose.orientation.w = new_w
        
    if msg.data == "A":
        navigator.info('新目标点：A点')
        
        current_pose = Pose()
        new_x = 2.0
        new_y = 3.14
        new_z = -0.00534
        new_w = 1.0

        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = new_x
        goal_pose.pose.position.y = new_y
        goal_pose.pose.position.z = new_z
        goal_pose.pose.orientation.w = new_w

        # 设置目标点后，让主循环去执行导航

    new_goal_pose = goal_pose
    new_goal_pose_str = f'New Goal Pose: ({new_goal_pose.pose.position.x}, {new_goal_pose.pose.position.y}, {new_goal_pose.pose.orientation.w})'
    navigator.info(new_goal_pose_str)

def main():

    global new_goal_pose  # 声明为全局变量
    new_goal_pose = None
    rclpy.init()
    
    navigator = BasicNavigator() 
    #ros2话题接收
    #node = rclpy.Node('waypoint_receive_node')
    node = rclpy.create_node('waypoint_receive_node')
    # 创建 QoS 配置
    qos_profile = QoSProfile(depth=10)
    # 创建订阅者
    subscription = node.create_subscription(
        msg_type=String,
        topic='waypoint_topic',
        #callback=lambda msg: my_callback(msg, navigator),
        callback=functools.partial(my_callback, navigator=navigator),  # 使用 functools.partial 传递 navigator
        qos_profile=qos_profile)
        
        
    
    # Set our demo's initial pose
    initial_pose = Pose()
    initial_pose.position.x = 3.45
    initial_pose.position.y = 2.15
    initial_pose.orientation.z = 1.0
    initial_pose.orientation.w = 0.0
    navigator.setInitialPose(initial_pose)
    
    # Wait for navigation to fully activate
    #navigator.waitUntilNav2Active()
    navigator.info('到达循环')
    # Go to our demos first goal pose
    while True:
        #接收话题消息
        navigator.info('进入循环，准备接收话题消息')
        rclpy.spin_once(node, timeout_sec=3)
        navigator.info('跳出回调函数')
        navigator.info("检查 new_goal_pose 内容：{}".format(new_goal_pose))
        if new_goal_pose is not None:
            navigator.info('发送新的路标点')
            navigator.goToPose(new_goal_pose)
            new_goal_pose = None  # 重置，避免重复导航
        #exit(0)
        
    # 关闭节点和 rclpy
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

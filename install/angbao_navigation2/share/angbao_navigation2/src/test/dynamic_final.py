# -*- coding: utf-8 -*-
import time
import pyrealsense2 as rs
import numpy as np
import cv2 as cv
from sensor_msgs.msg import Image, CameraInfo
import tf2_ros
from geometry_msgs.msg import PointStamped, TransformStamped
from tf2_geometry_msgs import PointStamped as TFPointStamped
from rclpy.time import Time
import rclpy
from rclpy.node import Node
from nav_to_pose import BasicNavigator
from geometry_msgs.msg import PoseStamped,Twist
import rospy

class RealsenseCamera:
    def shutdown():
        twist = Twist()
        twist.linear.x = 0
        twist.angular.z = 0
        cmd_vel_Publisher.publish(twist)
        print("stop")

    def __init__(self, node):
        # 定义流程pipeline，创建一个管道
        self.pipeline = rs.pipeline()
        # 定义配置config
        self.config = rs.config()
        # 配置depth流
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
        # 配置color流
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
        # streaming流开始
        self.pipe_profile = self.pipeline.start(self.config)
        # align_to 是计划对齐深度帧的流类型
        self.align_to = rs.stream.color
        # rs.align 执行深度帧与其他帧的对齐
        self.align = rs.align(self.align_to)

        # Initialize TF buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, node)

    # 获取对齐图像帧与相机参数
    def get_aligned_images(self):
        # 等待获取图像帧，获取颜色和深度的框架集
        frames = self.pipeline.wait_for_frames()
        # 获取对齐帧，将深度框与颜色框对齐
        aligned_frames = self.align.process(frames)
        # 获取对齐帧中的的depth帧
        aligned_depth_frame = aligned_frames.get_depth_frame()
        # 获取对齐帧中的的color帧
        aligned_color_frame = aligned_frames.get_color_frame()
        # 获取深度参数（像素坐标系转相机坐标系会用到）
        depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        # 获取相机内参
        color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics
        # RGB图
        img_color = np.asanyarray(aligned_color_frame.get_data())
        # 深度图（默认16位）
        img_depth = np.asanyarray(aligned_depth_frame.get_data())
        return color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame


if __name__ == "__main__":
    rclpy.init()  # 初始化 ROS 节点
    node = rclpy.create_node('realsense_camera_node')  # 创建 ROS 节点

    cmd_vel_Publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    camera = RealsenseCamera(node)
    while True:
        # 获取对齐图像帧与相机参数
        color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = camera.get_aligned_images()
        
        # 将彩色图像从 RGB 格式转换为 BGR 格式
        #cv_image = cv.cvtColor(img_color, cv.COLOR_RGB2BGR)
        cv_image = img_color

        # 定义结构元素
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

        # 定义蓝色的HSV范围
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])

        #lower_blue = np.array([0, 0, 0])
        #upper_blue = np.array([180, 255, 30])

        #lower_blue = np.array([0, 100, 100])
        #upper_blue = np.array([10, 255, 255])


        # 将图像转换为HSV颜色空间
        hsv_frame = cv.cvtColor(cv_image, cv.COLOR_BGR2HSV)

        # 创建蓝色的掩码
        mask = cv.inRange(hsv_frame, lower_blue, upper_blue)
        mask2 = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask3 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernel)

        # 找出面积最大的区域
        contours, _ = cv.findContours(mask3, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


        maxArea = 0
        maxIndex = 0
        for i, c in enumerate(contours):
            area = cv.contourArea(c)
            if area > maxArea:
                maxArea = area
                maxIndex = i

        # 绘制矩形和中心点
        if contours:
            x, y, w, h = cv.boundingRect(contours[maxIndex])
            cv.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            center_x = int(x + w/2)
            center_y = int(y + h/2)
            dis = aligned_depth_frame.get_distance(center_x, center_y) 
            print ('depth: ',dis)
            cv.circle(cv_image, (center_x, center_y), 5, (0, 0, 255), -1)

            # 根据中心点位置进行简单的运动控制反馈
            screen_center = cv_image.shape[1] / 2
            offset = 50
            if center_x < screen_center - offset:
                print("turn left")
                

            elif screen_center - offset <= center_x <= screen_center + offset:
                print("keep")
            elif center_x > screen_center + offset:
                Twist.cmd_vel_msg.angular.z = -0.1
                #print("turn right")

            # 显示图像和掩码
            cv.imshow("mask4", mask3)
            cv.imshow("frame", cv_image)
            cv.waitKey(1)

       

        
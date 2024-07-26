#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
import tf2_ros
from geometry_msgs.msg import PointStamped, TransformStamped
from tf2_geometry_msgs import PointStamped as TFPointStamped
from nav_to_pose import BasicNavigator
import time
from geometry_msgs.msg import PoseStamped
import cv_bridge
import numpy as np
import pyrealsense2 as rs
import cv2

class DepthToWorldConverter(Node):
    def __init__(self):
        super().__init__('depth_to_world_converter')
        self.get_logger().info("Initializing Depth To World Converter node...")

        self.fx = None
        self.fy = None
        self.cx = None
        self.cy = None

        self.subscription_depth_info = self.create_subscription(
            CameraInfo,
            '/camera/aligned_depth_to_color/camera_info',
            self.camera_info_callback,
            10)
          
        self.subscription_depth = self.create_subscription(
            Image,
            '/camera/aligned_depth_to_color/image_raw',
            self.depth_callback,
            10)    
        
        # Initialize TF buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        #self.subscription  # 避免 unused variable 警告
        self.bridge = cv_bridge.CvBridge()
         

    def camera_info_callback(self, msg):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]

    def depth_callback(self, msg):
        if self.fx is not None:
            # 将 ROS 消息转换为 OpenCV 格式
            depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            # 获取深度图像的尺寸
            height, width = depth_image.shape
            if height == 480 and width == 848:
                return
            print("depth_image.shape:",depth_image.shape)
            # 计算图像中心点像素的坐标
            pixel_x = width // 2
            pixel_y = height // 2
            pixel_x = 320
            pixel_y = 360
            depth_pixel = (pixel_x,pixel_y)
            
            # 获取中心点像素的深度值
            dis = depth_image[pixel_y, pixel_x]/1000
            print("Depth at center pixel: ", dis,"米")

            camera_coordinate_x = (depth_pixel[0] - self.cx) * dis / self.fx
            camera_coordinate_y = (depth_pixel[1] - self.cy) * dis / self.fy
            camera_coordinate_z = dis

            camera_coordinate = (camera_coordinate_x, camera_coordinate_y, camera_coordinate_z)
            print("Camera coordinate:", camera_coordinate)
            

            # Use camera coordinates X_c, Y_c, Z_c as needed
            camera_point = PointStamped()
            camera_point.header.frame_id = "camera_color_optical_frame"
            camera_point.point.x = camera_coordinate_x
            camera_point.point.y = camera_coordinate_y
            camera_point.point.z = camera_coordinate_z

            # Use camera coordinates X_c, Y_c, Z_c as needed
            print("Pixel ({}, {}): Camera Coordinate ({}, {}, {})".format(pixel_x, pixel_y,camera_coordinate_x, camera_coordinate_y, camera_coordinate_z))
            map_point = self.convert_camera_to_map(camera_point)
            if map_point:
                print("Camera Point (camera_link) - X: {}, Y: {}, Z: {}".format(camera_point.point.x, camera_point.point.y, camera_point.point.z))
                print("Map Point (map_frame) - X: {}, Y: {}, Z: {}".format(map_point.point.x, map_point.point.y, map_point.point.z)) 

    def convert_camera_to_map(self, camera_point):
        try:
            # Lookup transform from camera frame to map frame
            #transform = self.tf_buffer.lookup_transform(
            #    "map", camera_point.header.frame_id, rclpy.time.Time())
            
            transform = self.tf_buffer.lookup_transform(
                "map", "camera_color_optical_frame",  # 从test1到test2的变换
                rclpy.time.Time())
            #print("Transform found: %s", transform)

            #transform = self.tf_buffer.lookup_transform(
            #    "test1", "test2",  # 从test1到test2的变换
            #    rclpy.time.Time())
            #print("test1totest2_Transform found: %s", transform)

            # Transform camera_point to map frame
            tf_camera_point = TFPointStamped()
            tf_camera_point.header.frame_id = camera_point.header.frame_id
            tf_camera_point.point = camera_point.point
            map_point = self.tf_buffer.transform(tf_camera_point, "map")

            return map_point

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error("Failed to transform camera point to map: %s" % e)
            return None        
        
def main(args=None):
    rclpy.init(args=args)
    node = DepthToWorldConverter()
    node.get_logger().info("Depth To World Converter node created.")
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

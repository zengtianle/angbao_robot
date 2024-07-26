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
            '/camera/depth/camera_info',
            self.camera_info_callback,
            10)
          
        self.subscription_depth = self.create_subscription(
            Image,
            # '/camera/color/image_raw',
            '/camera/depth/image_rect_raw',
            self.depth_callback,
            10)    
        
        # Initialize TF buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
         

    def camera_info_callback(self, msg):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]

    def depth_callback(self, msg):
        if self.fx is not None:
            pixel_x = 424 # Example pixel x-coordinate
            pixel_y = 240 # Example pixel y-coordinate

            # print(msg.width)

            # Extract depth value from the image data
            index = (pixel_y * msg.width) + pixel_x
            depth_value = msg.data[index] / 255 

            # Convert pixel coordinates to camera coordinates
            X_c = (pixel_x - self.cx) * depth_value / self.fx
            Y_c = (pixel_y - self.cy) * depth_value / self.fy
            Z_c = depth_value

            # Use camera coordinates X_c, Y_c, Z_c as needed
            camera_point = PointStamped()
            camera_point.header.frame_id = "camera_link"
            camera_point.point.x = X_c
            camera_point.point.y = Y_c
            camera_point.point.z = Z_c

            # Use camera coordinates X_c, Y_c, Z_c as needed
            print("Pixel ({}, {}): Camera Coordinate ({}, {}, {})".format(pixel_x, pixel_y, X_c, Y_c, Z_c))
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
                "laser_frame", "camera_link",  # 从test1到test2的变换
                rclpy.time.Time())
            #print("Transform found: %s", transform)

            transform = self.tf_buffer.lookup_transform(
                "test1", "test2",  # 从test1到test2的变换
                rclpy.time.Time())
            print("test1totest2_Transform found: %s", transform)

            # Transform camera_point to map frame
            tf_camera_point = TFPointStamped()
            tf_camera_point.header.frame_id = camera_point.header.frame_id
            tf_camera_point.point = camera_point.point
            map_point = self.tf_buffer.transform(tf_camera_point, "laser_frame")

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

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv_bridge
import numpy as np
import cv2

class DepthImageSubscriber(Node):

    def __init__(self):
        super().__init__('depth_image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/aligned_depth_to_color/image_raw',  # 深度图像话题
            self.depth_image_callback,
            10)
        self.subscription  # 避免 unused variable 警告
        self.bridge = cv_bridge.CvBridge()

    def depth_image_callback(self, msg):
        try:
            # 将 ROS 消息转换为 OpenCV 格式
            depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

            # 调整图像尺寸为640x480
            depth_image = cv2.resize(depth_image, (640, 480))
            # 获取深度图像的尺寸
            height, width = depth_image.shape
            print("depth_image.shape:",depth_image.shape)
            # 计算图像中心点像素的坐标
            center_x = width // 2
            center_y = height // 2
            # 获取中心点像素的深度值
            depth_at_center = depth_image[center_y, center_x]/1000
            print("Depth at center pixel: ", depth_at_center)
        except Exception as e:
            print("Error:", e)

def main(args=None):
    rclpy.init(args=args)
    depth_image_subscriber = DepthImageSubscriber()
    rclpy.spin(depth_image_subscriber)
    depth_image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

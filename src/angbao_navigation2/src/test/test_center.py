import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge

class DepthListener(Node):
    def __init__(self):
        super().__init__('depth_listener')
        self.bridge = CvBridge()
        self.subscription_depth = self.create_subscription(
            Image,
            '/camera/depth/image_rect_raw',  # 深度图像话题
            self.depth_callback,
            10)
        self.subscription_info = self.create_subscription(
            CameraInfo,
            '/camera/depth/camera_info',  # 相机信息话题
            self.info_callback,
            10)
        self.intrinsics = None

    def depth_callback(self, msg):
      if self.intrinsics is None:
        self.get_logger().warn("Camera intrinsics not yet received.")
        return

      depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    # 计算中心点像素的深度值
      center_x = depth_image.shape[1] // 2
      center_y = depth_image.shape[0] // 2
      center_depth = depth_image[center_y, center_x]

      self.get_logger().info("Center pixel depth (mm): %s", str(center_depth))


    def info_callback(self, msg):
        self.intrinsics = msg

def main(args=None):
    rclpy.init(args=args)
    depth_listener = DepthListener()
    rclpy.spin(depth_listener)
    depth_listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

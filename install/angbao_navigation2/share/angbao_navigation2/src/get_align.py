import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
 
class ImageSynchronizer(Node):
    def __init__(self):
        super().__init__('image_synchronizer')
        self.has_been_called = False
        self.last_header = None

        self.sub_image1 = self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.image1_callback,
            10)
        self.sub_image2 = self.create_subscription(
            Image,
            '/camera/depth/image_raw',
            self.image2_callback,
            10)
 
    def image1_callback(self, msg):
        if self.has_been_called:
            self.has_been_called = False
            self.get_logger().info(
                'Image1 timestamp: %s, Image2 timestamp: %s' %
                (msg.header.stamp.sec, self.last_header.stamp.sec))
 
    def image2_callback(self, msg):
        self.has_been_called = True
        self.last_header = msg.header
        if self.has_been_called:
            self.get_logger().info(
                'Image1 timestamp: %s, Image2 timestamp: %s' %
                (self.last_header.stamp.sec, msg.header.stamp.sec))
 
def main(args=None):
    rclpy.init(args=args)
    synchronizer = ImageSynchronizer()
    rclpy.spin(synchronizer)
    rclpy.shutdown()
 
if __name__ == '__main__':
    main()

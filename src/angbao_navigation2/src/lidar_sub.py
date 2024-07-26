import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LaserSubscriber(Node):

    def __init__(self):
        super().__init__('laser_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10)

    def laser_callback(self, msg):
        ranges = msg.ranges
        # 获取前方的距离（假设雷达数据是从正前方开始的）
        front_distance = ranges[len(ranges)//2]
        # 打印前方的距离信息
        self.get_logger().info('Front distance: %f' % front_distance)

def main(args=None):
    rclpy.init(args=args)
    laser_subscriber = LaserSubscriber()
    rclpy.spin(laser_subscriber)
    laser_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

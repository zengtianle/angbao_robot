import rclpy
from rclpy.node import Node
import tf2_ros
import geometry_msgs.msg


class TFPublisher(Node):

    def __init__(self):
        super().__init__('tf_publisher')
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # 创建测试变换
        self.transform = geometry_msgs.msg.TransformStamped()
        self.transform.header.frame_id = 'test1'
        self.transform.child_frame_id = 'test2'
        self.transform.transform.translation.x = 1.0
        self.transform.transform.translation.y = 2.0
        self.transform.transform.translation.z = 3.0
        self.transform.transform.rotation.x = 0.0
        self.transform.transform.rotation.y = 0.0
        self.transform.transform.rotation.z = 0.0
        self.transform.transform.rotation.w = 1.0

        # 发布测试变换
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        # 发布频率
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.publish_tf)

    def publish_tf(self):
        self.transform.header.stamp = self.get_clock().now().to_msg()
        self.tf_broadcaster.sendTransform(self.transform)

        # 查找变换
        try:
            transform = self.tf_buffer.lookup_transform(
                "test1", "test2",  # 从test1到test2的变换
                rclpy.time.Time())
            print("Transform found: %s", transform)
        except tf2_ros.LookupException as e:
            print("Failed to lookup transform: %s", e)


def main(args=None):
    rclpy.init(args=args)
    tf_publisher = TFPublisher()
    rclpy.spin(tf_publisher)
    tf_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

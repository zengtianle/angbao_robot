import rclpy
from std_msgs.msg import String
import time

rclpy.init()
node = rclpy.create_node('text_publisher_node')
publisher = node.create_publisher(String, 'waypoint_topic', 10)
msg = String()

def publish_to_ros(result):
    msg.data = result
    node.get_logger().info('Publishing: %s' % msg.data)
    publisher.publish(msg)

if __name__ == "__main__":
    while True:
        publish_to_ros("A")
        rclpy.spin_once(node, timeout_sec=5.0)
        publish_to_ros("B")
        time.sleep(2)  

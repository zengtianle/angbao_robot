import rclpy
from rclpy.node import Node
import tf2_ros
from geometry_msgs.msg import TransformStamped

class StaticTFPublisher(Node):
    def __init__(self):
        super().__init__('static_tf_publisher')
        
        # Create a StaticTransformBroadcaster
        self.tf_broadcaster = tf2_ros.StaticTransformBroadcaster(self)
        
        # Publish the static TF transform from camera to lidar
        self.publish_camera_to_lidar_tf()

    def publish_camera_to_lidar_tf(self):
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'camera_link'  # Parent frame
        transform.child_frame_id = 'laser_frame'  # Child frame

        # Set the translation
        transform.transform.translation.x = 1.0  # Example translation along x-axis
        transform.transform.translation.y = 0.5  # Example translation along y-axis
        transform.transform.translation.z = 0.0  # Example translation along z-axis

        # Set the rotation (quaternion)
        transform.transform.rotation.x = 0.0  # Example quaternion x
        transform.transform.rotation.y = 0.0  # Example quaternion y
        transform.transform.rotation.z = 0.0  # Example quaternion z
        transform.transform.rotation.w = 1.0  # Example quaternion w (unit quaternion)

        # Publish the static TF transform
        self.tf_broadcaster.send_transform_static(transform)

def main(args=None):
    rclpy.init(args=args)
    static_tf_publisher = StaticTFPublisher()
    rclpy.spin(static_tf_publisher)
    static_tf_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

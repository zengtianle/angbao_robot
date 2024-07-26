import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
import tf2_ros
import numpy as np
from scipy.spatial.transform import Rotation as R


class CameraTFPublisher(Node):
    def __init__(self):
        super().__init__('camera_tf_publisher')
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.publish_tf)
        
    def rotation_matrix_to_quaternion(self,rot_matrix):
        r = R.from_matrix(rot_matrix)
        quaternion = r.as_quat()
        return quaternion
        
    def publish_tf(self):
        # Define the transform from camera_link to laser_frame
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'laser_frame'
        transform.child_frame_id = 'camera_link'
        
        # Fill the transformation matrix
        transform_matrix = [
            7.0842658844480155e-02, 2.1967225457715578e-01, 9.7299815943137014e-01, -2.4747704487777056e-01,
            -9.9514252517732238e-01, 8.2411354264238623e-02, 5.3849078655410665e-02, 4.4355727734253239e-02,
            -6.8356947500214316e-02, -9.7208665727769539e-01, 2.2444344158635932e-01, 2.0377320541182423e-01,
            0., 0., 0., 1.
        ]
        
        # 提取平移向量
        translation_vector = np.array([transform_matrix[3], transform_matrix[7], transform_matrix[11]])

        
        # Fill the translation
        transform.transform.translation.x = transform_matrix[3]
        transform.transform.translation.y = transform_matrix[7]
        transform.transform.translation.z = transform_matrix[11]
        
        rotation_matrix=np.array([[7.0842658844480155e-02,2.1967225457715578e-01,9.7299815943137014e-01],
                          [-9.9514252517732238e-01,8.2411354264238623e-02,5.3849078655410665e-02],
                          [-6.8356947500214316e-02,-9.7208665727769539e-01,2.2444344158635932e-01]])
        
        
        
        # 将旋转矩阵转换为四元数
        quaternion = self.rotation_matrix_to_quaternion(rotation_matrix)
        
        # Fill the rotation
        transform.transform.rotation.x = quaternion[0]
        transform.transform.rotation.y = quaternion[1]
        transform.transform.rotation.z = quaternion[2]
        transform.transform.rotation.w = quaternion[3]

        # Publish the transform
        self.tf_broadcaster.sendTransform(transform)
        
        self.get_logger().info("Published TF transform:\n{}".format(transform))

def main(args=None):
    rclpy.init(args=args)
    camera_tf_publisher = CameraTFPublisher()
    rclpy.spin(camera_tf_publisher)
    camera_tf_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

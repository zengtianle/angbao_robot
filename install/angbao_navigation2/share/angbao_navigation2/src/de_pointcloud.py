import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import pcl

class PointCloudFilter(Node):
    def __init__(self):
        super().__init__('point_cloud_filter')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/camera/camera/depth/color/points',  # 替换成你的点云话题
            self.pointcloud_callback,
            10)

    def pointcloud_callback(self, msg):
        # 将PointCloud2消息转换为PCL点云对象
        pcl_cloud = pcl.PointCloud()
        pcl_cloud.from_msg(msg)

        # 在这里添加你的滤波处理逻辑，比如移除离群点、下采样等
        # 例如，使用VoxelGrid下采样
        sor = pcl_cloud.make_voxel_grid_filter()
        sor.set_leaf_size(0.01, 0.01, 0.01)
        filtered_cloud = sor.filter()

        # 将滤波后的PCL点云对象转换为PointCloud2消息
        filtered_cloud_msg = filtered_cloud.to_msg()

        # 发布滤波后的点云数据
        # 替换成你的发布话题
        self.publisher_.publish(filtered_cloud_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudFilter()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


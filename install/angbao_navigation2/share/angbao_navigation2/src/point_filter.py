import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import pcl
from std_msgs.msg import Header

class FilterAndPublish(Node):

    def __init__(self):
        super().__init__('pcl_filtering')
        self.pub = self.create_publisher(PointCloud2, '/points_filtered', 1)
        self.sub = self.create_subscription(PointCloud2, '/camera/camera/depth/color/points', self.callback, 1)
        self.thresh = 15  # This is the minimum number of points that have to occupy a voxel in order for it to survive the downsample.

    def callback(self, msg):
        print("ok!")
        cloud = pcl.PointCloud.PointXYZ()
        pcl.fromROSMsg(msg, cloud)

        # What to do here: 
        # 1. Take cloud and put it in a voxel grid while restricting the bounding box
        # 2. Go through the voxels and remove all points in a voxel that has less than this.thresh points
        # 3. Publish resulting cloud

        vox = pcl.filters.VoxelGrid.PointXYZ()
        vox.setInputCloud(cloud)
        # The leaf size is the size of voxels pretty much. Note that this value affects what a good threshold value would be.
        vox.setLeafSize(0.05, 0.05, 0.05)
        # I limit the overall volume being considered so lots of "far away" data that is just terrible doesn't even have to be considered.
        vox.setFilterLimits(-1.0, 1.0)
        # The line below is perhaps the most important as it reduces ghost points.
        vox.setMinimumPointsNumberPerVoxel(self.thresh)

        cloud_filtered = pcl.PointCloud.PointXYZ()
        vox.filter(cloud_filtered)

        cloud_filtered_msg = pcl.PointCloud2()
        pcl.toROSMsg(cloud_filtered, cloud_filtered_msg)
        cloud_filtered_msg.header = Header(frame_id=msg.header.frame_id)

        self.pub.publish(cloud_filtered_msg)

def main(args=None):
    rclpy.init(args=args)
    filter_and_publish = FilterAndPublish()
    rclpy.spin(filter_and_publish)
    filter_and_publish.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


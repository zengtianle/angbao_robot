from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import rclpy
from rclpy.duration import Duration
import rospy

def main():
    rclpy.init()
    # 初始化 ROS
    rospy.init_node("basic_navigator")

    # 创建 basic_navigator 对象
    navigator = rospy.Publisher("basic_navigator", String, queue_size=10)
    # 设置目标点坐标
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = rospy.Time.now()
    goal_pose.pose.position.x = 1.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 1.0


    print("Waiting for 'NavigateToPose' action server")

    print(goal_pose.header.stamp)

    #navigator.debug("Waiting for 'NavigateToPose' action server")
    #while not navigator.nav_to_pose_client.wait_for_server(timeout_sec=1.0):
    #    navigator.info("'NavigateToPose' action server not available, waiting...")

    # Now you might want to call your navigation method (goToPose) if it's defined in BasicNavigator class
    #success = navigator.goToPose(goal_pose)
    #if success:
    #    navigator.info("Navigation to the goal succeeded.")
    #else:
    #    navigator.error("Navigation to the goal failed.")

    rclpy.shutdown()

if __name__ == '__main__':
    main()

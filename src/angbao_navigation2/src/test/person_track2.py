import cv2 as cv
from geometry_msgs.msg import Twist
from test2_ros_depth import RealsenseCamera
import rclpy
from rclpy.node import Node
import numpy as np

class FollowNode(Node):
    def __init__(self):
        super().__init__('follow_node')
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 1)
        #self.camera = RealsenseCamera(self)
        #self.tracker = cv.TrackerCSRT_create()


        self.Max_linear_speed = 0.3
        self.Min_linear_speed = 0.1
        self.Min_distance = 1.5
        self.Max_distance = 5
        self.Max_rotation_speed = 0.75

        self.k_linear_speed = (self.Max_linear_speed - self.Min_linear_speed) / (self.Max_distance - self.Min_distance)
        self.h_linear_speed = self.Min_linear_speed - self.k_linear_speed * self.Min_distance

        self.k_rotation_speed = 0.004
        self.h_rotation_speed_left = 1.2
        self.h_rotation_speed_right = 1.36

        self.ERROR_OFFSET_X_left1 = 100
        self.ERROR_OFFSET_X_left2 = 300
        self.ERROR_OFFSET_X_right1 = 340
        self.ERROR_OFFSET_X_right2 = 540

        self.linear_speed = 0.0
        self.rotation_speed = 0.0

        self.dist_val = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.selectRect = None
        self.result = None
        self.select_flag = False
        self.bRenewROI = False
        self.bBeginKCF = False
        self.enable_get_depth = False

        self.screen_center = None
        



    def shutdown_signal_handler(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_publisher.publish(twist)
        print("Stop")

    def run(self,result,img,img_depth):
        while rclpy.ok():
            result[2] = result[2]-result[0]
            result[3] = result[3]-result[1]
            #color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = self.camera.get_aligned_images()
            
            self.dist_val[0] = 0.001 * img_depth[result[1] + result[3] // 3, result[0] + result[2] // 3]
            self.dist_val[1] = 0.001 * img_depth[result[1] + result[3] // 3, result[0] + 2 * result[2] // 3]
            self.dist_val[2] = 0.001 * img_depth[result[1] + 2 * result[3] // 3, result[0] + result[2] // 3]
            self.dist_val[3] = 0.001 * img_depth[result[1] + 2 * result[3] // 3, result[0] + 2 * result[2] // 3]
            self.dist_val[4] = 0.001 * img_depth[result[1] + result[3] // 2, result[0] + result[2] // 2]

            distance = 0.0
            num_depth_points = 5
            for val in self.dist_val:
                if 0.6 > val:
                    self.shutdown_signal_handler()
                if 0.6 < val < 10.0:
                    distance += val
                else:
                    num_depth_points -= 1
                    
            if num_depth_points > 0:   
                distance /= num_depth_points

            if distance > self.Min_distance:
                self.linear_speed = distance * self.k_linear_speed + self.h_linear_speed
            else:
                self.linear_speed = 0.0

            if self.linear_speed > self.Max_linear_speed:
                self.linear_speed = self.Max_linear_speed

            center_x = result[0] + result[2] // 2
            if center_x < self.ERROR_OFFSET_X_left1:
                self.rotation_speed = self.Max_rotation_speed
            elif self.ERROR_OFFSET_X_left1 < center_x < self.ERROR_OFFSET_X_left2:
                self.rotation_speed = -self.k_rotation_speed * center_x + self.h_rotation_speed_left
            elif self.ERROR_OFFSET_X_right1 < center_x < self.ERROR_OFFSET_X_right2:
                self.rotation_speed = -self.k_rotation_speed * center_x + self.h_rotation_speed_right
            elif center_x > self.ERROR_OFFSET_X_right2:
                self.rotation_speed = -self.Max_rotation_speed
            else:
                self.rotation_speed = 0.0

            print("distance =", distance)
            
            
            twist = Twist()
            twist.linear.x = self.linear_speed
            twist.angular.z = self.rotation_speed
            print("线速度={}, 角速度={}".format(twist.linear.x, twist.angular.z))

            # self.cmd_vel_publisher.publish(twist)

            if cv.waitKey(1) == ord('q'):
                break

        self.shutdown_signal_handler()

# def main():
#     rclpy.init()
#     node = FollowNode()
#     try:
#         node.run()
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()

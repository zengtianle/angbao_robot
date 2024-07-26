import cv2 as cv
from geometry_msgs.msg import Twist
from test2_ros_depth import RealsenseCamera
import rclpy
from rclpy.node import Node
import numpy as np
from nav_to_pose import BasicNavigator
from geometry_msgs.msg import PoseStamped
from tf2_geometry_msgs import PointStamped as TFPointStamped
from geometry_msgs.msg import PointStamped
import tf2_ros
import time

class FollowNode(Node):
    def __init__(self):
        super().__init__('follow_node')
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 1)
        self.camera = RealsenseCamera(self)
        self.tracker = cv.TrackerCSRT_create()
        self.navigator = BasicNavigator()
        
        self.fx = 419.33795
        self.fy = 419.33795
        self.cx = 420.72561
        self.cy = 238.68894


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
        #self.selectRect = (100, 200, 50, 50)
        
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
    def convert_camera_to_map(self, camera_point):
        try:
            transform = self.tf_buffer.lookup_transform(
                "map", "camera_color_optical_frame", 
                rclpy.time.Time())
            # Transform camera_point to map frame
            tf_camera_point = TFPointStamped()
            tf_camera_point.header.frame_id = camera_point.header.frame_id
            tf_camera_point.point = camera_point.point
            map_point = self.tf_buffer.transform(tf_camera_point, "map")
            return map_point
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error("Failed to transform camera point to map: %s" % e)
            return None     
        
    def pixel_to_camera_to_map(self,depth_image,pixel_x,pixel_y,dis):
        if self.fx is not None:
            # 获取深度图像的尺寸
            # height, width = depth_image.shape
            # if height == 480 and width == 848:
            #     return
            #print("depth_image.shape:",depth_image.shape)
            # 计算图像中心点像素的坐标
            depth_pixel = (pixel_x,pixel_y)

            camera_coordinate_x = (depth_pixel[0] - self.cx) * dis / self.fx
            camera_coordinate_y = (depth_pixel[1] - self.cy) * dis / self.fy
            camera_coordinate_z = dis

            camera_coordinate = (camera_coordinate_x, camera_coordinate_y, camera_coordinate_z)
            print("Camera coordinate:", camera_coordinate)
            

            # Use camera coordinates X_c, Y_c, Z_c as needed
            camera_point = PointStamped()
            camera_point.header.frame_id = "camera_color_optical_frame"
            camera_point.point.x = camera_coordinate_x
            camera_point.point.y = camera_coordinate_y
            camera_point.point.z = camera_coordinate_z

            # Use camera coordinates X_c, Y_c, Z_c as needed
            print("Pixel ({}, {}): Camera Coordinate ({}, {}, {})".format(pixel_x, pixel_y,camera_coordinate_x, camera_coordinate_y, camera_coordinate_z))
            map_point = self.convert_camera_to_map(camera_point)
            if map_point:
                print("Camera Point (camera_link) - X: {}, Y: {}, Z: {}".format(camera_point.point.x, camera_point.point.y, camera_point.point.z))
                print("Map Point (map_frame) - X: {}, Y: {}, Z: {}".format(map_point.point.x, map_point.point.y, map_point.point.z)) 
            #return map_point

    def onMouse(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.bBeginKCF = False
            self.select_flag = True
            self.origin = (x, y)
            self.selectRect = (x, y, 0, 0)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.select_flag:
                self.selectRect = (self.origin[0], self.origin[1], x - self.origin[0], y - self.origin[1])

        elif event == cv.EVENT_LBUTTONUP:
            self.select_flag = False
            self.bRenewROI = True
            
            


    def shutdown_signal_handler(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_publisher.publish(twist)
        print("Stop")

    def run(self):
        while rclpy.ok():
            color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = self.camera.get_aligned_images()
            
            # 选择要跟踪的初始位置
            #bbox = cv.selectROI(img_color, False)

            if self.selectRect:
                if self.bRenewROI:                                 
                    self.tracker.init(img_color, self.selectRect)
                    self.bBeginKCF = True
                    self.bRenewROI = False
                    self.enable_get_depth = False

                if self.bBeginKCF:
                    ok, self.result = self.tracker.update(img_color)
                    if ok:
                        self.enable_get_depth = True
                        print("updated:",self.result)
                        # 更新矩形框的位置为跟踪到的目标位置和大小
                        x, y, w, h = self.result
                        self.selectRect = (int(x), int(y), int(w), int(h))
                        self.center_x = (x + (x + w)) / 2
                        self.center_y = (y + (y + h)) / 2
                        self.pixel = (self.center_x,self.center_y)
                        print("pixel:",self.pixel)
                        cv.rectangle(img_color, (x, y), (x + w, y + h), (0, 255, 0), 2)

                else:
                    
                    cv.rectangle(img_color, self.selectRect, (255, 0, 0), 2)

                if self.enable_get_depth:
                    '''
                    self.dist_val[0] = 0.001 * img_depth[self.result[1] + self.result[3] // 3, self.result[0] + self.result[2] // 3]
                    self.dist_val[1] = 0.001 * img_depth[self.result[1] + self.result[3] // 3, self.result[0] + 2 * self.result[2] // 3]
                    self.dist_val[2] = 0.001 * img_depth[self.result[1] + 2 * self.result[3] // 3, self.result[0] + self.result[2] // 3]
                    self.dist_val[3] = 0.001 * img_depth[self.result[1] + 2 * self.result[3] // 3, self.result[0] + 2 * self.result[2] // 3]
                    self.dist_val[4] = 0.001 * img_depth[self.result[1] + self.result[3] // 2, self.result[0] + self.result[2] // 2]
                    '''
                    self.dist_val[0] = aligned_depth_frame.get_distance(self.result[1] + self.result[3] // 3, self.result[0] + self.result[2] // 3)
                    self.dist_val[1] = aligned_depth_frame.get_distance(self.result[1] + self.result[3] // 3, self.result[0] + 2 * self.result[2] // 3)
                    self.dist_val[2] = aligned_depth_frame.get_distance(self.result[1] + 2 * self.result[3] // 3, self.result[0] + self.result[2] // 3)
                    self.dist_val[3] = aligned_depth_frame.get_distance(self.result[1] + 2 * self.result[3] // 3, self.result[0] + 2 * self.result[2] // 3)
                    self.dist_val[4] = aligned_depth_frame.get_distance(self.result[1] + self.result[3] // 2, self.result[0] + self.result[2] // 2)

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
                        
                        map_point = self.pixel_to_camera_to_map(aligned_depth_frame,self.pixel[0],self.pixel[1],distance)
                        #执行导航操作
                        goal_pose = PoseStamped()
                        goal_pose.header.frame_id = 'map'
                        goal_pose.header.stamp = self.get_clock().now().to_msg()
                        goal_pose.pose.position.x = map_x # 您的目标点 x 坐标
                        goal_pose.pose.position.y = map_y  # 您的目标点 y 坐标
                        goal_pose.pose.position.z = map_z
                        goal_pose.pose.orientation.w = 1.0
                        self.navigator.info('导航到目标点')
                        self.navigator.goToPose(goal_pose)

                        #等待导航完成
                        while not self.navigator.isNavComplete():
                            time.sleep(1)
                    else:
                        self.linear_speed = 0.0

                    if self.linear_speed > self.Max_linear_speed:
                        self.linear_speed = self.Max_linear_speed

                    center_x = self.result[0] + self.result[2] // 2
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

            #self.cmd_vel_publisher.publish(twist)

            cv.imshow("RGB Image window", img_color)
            cv.setMouseCallback("RGB Image window", self.onMouse)

            if cv.waitKey(1) == ord('q'):
                break

        self.shutdown_signal_handler()

def main():
    rclpy.init()
    node = FollowNode()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

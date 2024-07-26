import cv2 as cv
from geometry_msgs.msg import Twist
from test2_ros_depth import RealsenseCamera
import rclpy
from rclpy.node import Node

class FollowNode(Node):
    def __init__(self):
        super().__init__('follow_node')
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 1)
        self.camera = RealsenseCamera(self)

        #self.lower_b = (65, 43, 46)
        #self.upper_b = (110, 255, 255)

        # 修改黄色的颜色范围
        self.lower_b = (20, 100, 100)
        self.upper_b = (40, 255, 255)


        self.height = 480
        self.width = 640
        self.screen_center = self.width / 2
        self.kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        self.offset = 50

    def shutdown_signal_handler(self):
        twist = Twist()
        twist.linear.x = 0
        twist.angular.z = 0
        self.cmd_vel_publisher.publish(twist)
        print("Stop")

    def run(self):
        while rclpy.ok():
            color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = self.camera.get_aligned_images()

            # 将图像转成HSV颜色空间
            hsv_frame = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
            # 基于颜色的物体提取
            mask = cv.inRange(hsv_frame, self.lower_b, self.upper_b)
            mask2 = cv.morphologyEx(mask, cv.MORPH_OPEN, self.kernel)
            mask3 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, self.kernel)

            # 找出面积最大的区域
            contours, _ = cv.findContours(mask3, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # 检查是否检测到了轮廓
            if contours:
                maxArea = 0
                maxIndex = 0
                for i, c in enumerate(contours):
                    area = cv.contourArea(c)
                    if area > maxArea:
                        maxArea = area
                        maxIndex = i
                # 绘制
                cv.drawContours(img_color, contours, maxIndex, (255, 255, 0), 2)
                # 获取外切矩形
                x, y, w, h = cv.boundingRect(contours[maxIndex])
                cv.rectangle(img_color, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # 获取中心像素点
                center_x = int(x + w / 2)
                center_y = int(y + h / 2)

                dis = aligned_depth_frame.get_distance(center_x, center_y) 
                print ('depth: ',dis)

                cv.circle(img_color, (center_x, center_y), 5, (0, 0, 255), -1)

                # 简单的打印反馈数据，之后补充运动控制
                twist = Twist()
                if center_x < self.screen_center - self.offset:
                    twist.linear.x = 0.00
                    twist.angular.z = 0.1
                    print("turn left")
                elif self.screen_center - self.offset <= center_x <= self.screen_center + self.offset:
                    if dis > 0.7:
                        twist.linear.x = 0.1
                        twist.angular.z = 0.0
                        print("foward")
                    else:
                        twist.linear.x = 0.00
                        twist.angular.z = 0.0
                        print("keep")
                elif center_x > self.screen_center + self.offset:
                    twist.linear.x = 0.00
                    twist.angular.z = -0.1
                    print("turn right")
                

                # 将速度发出
                self.cmd_vel_publisher.publish(twist)

                #cv.imshow("mask4", mask3)
                cv.imshow("frame", img_color)
                cv.putText(img_color,"Dis:"+str(dis)+" m", (center_x,center_y), cv.FONT_HERSHEY_SIMPLEX, 1.2,[0,0,255])
                cv.waitKey(1)
            else:
                #cv.imshow("mask4", mask3)
                twist = Twist()
                twist.angular.z = 0.05
                self.cmd_vel_publisher.publish(twist)
                cv.imshow("frame", img_color)
                #cv.putText(img_color,"Dis:"+str(dis)+" m", (center_x,center_y), cv.FONT_HERSHEY_SIMPLEX, 1.2,[0,0,255])
                cv.waitKey(1)
                print("No contours detected.")

        # 在退出循环时调用关闭处理程序
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

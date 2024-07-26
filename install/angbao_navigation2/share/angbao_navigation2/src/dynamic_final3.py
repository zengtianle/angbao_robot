import cv2 as cv
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from angbao_navigation2 import CustomDetection

class FollowNode(Node):
    def __init__(self):
        super().__init__('follow_node')
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 1)
        self.subscription = self.create_subscription(CustomDetection, 'detection_topic', self.callback, 1)
        self.bridge = CvBridge()

        self.screen_center = 320  # 假设标准宽度为640
        self.offset = 50
        self.depth_data = None

    def shutdown_signal_handler(self):
        twist = Twist()
        twist.linear.x = 0
        twist.angular.z = 0
        self.cmd_vel_publisher.publish(twist)
        print("停止")

    def callback(self, msg):
        
        if msg is  None:
            # 如果消息为空，打印警告信息并返回
            print("Received empty message!")
            return

        # 将彩色图像消息转换为 OpenCV 格式
        img_color = self.bridge.imgmsg_to_cv2(msg.image, desired_encoding='bgr8')
        x_1 = msg.anchors[0]
        y_1 = msg.anchors[1]
        x_2 = msg.anchors[2]
        y_2 = msg.anchors[3]
        #img_depth = self.bridge.imgmsg_to_cv2(msg.depth_image, desired_encoding='passthrough')

        center_x = (x_1 + x_2) / 2
        center_y = (y_1 + y_2) / 2

        # todo 
        depth_value = self.depth_data[center_y, center_x]  # 访问中心像素的深度值

        twist = Twist()

        while (center_x < self.screen_center - self.offset or center_x > self.screen_center + self.offset or depth_value > 0.7) :
            if center_x < self.screen_center - self.offset:
                twist.linear.x = 0.00
                twist.angular.z = 0.05
                print("向左转")
                    
            elif center_x > self.screen_center + self.offset:
                twist.linear.x = 0.00
                twist.angular.z = -0.05
                print("向右转")

            elif self.screen_center - self.offset <= center_x <= self.screen_center + self.offset:
                if depth_value > 0.7:
                    twist.linear.x = 0.05
                    twist.angular.z = 0.0
                    print("向前")
                else:
                    twist.linear.x = 0.00
                    twist.angular.z = 0.0
                    print("停止")
        

            self.cmd_vel_publisher.publish(twist)

            cv.imshow("frame", img_color)
            cv.putText(img_color,"Dis:"+str(depth_value)+" m", (center_x,center_y), cv.FONT_HERSHEY_SIMPLEX, 1.2,[0,0,255])
            cv.waitKey(1)

    def run(self):
        rclpy.spin(self)

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

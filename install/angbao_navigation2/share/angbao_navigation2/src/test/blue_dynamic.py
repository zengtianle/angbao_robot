import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
import cv2 as cv
import numpy as np

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/color/image_raw',  # 替换为你的图像话题
            self.image_callback,
            10)
        self.subscription  # 避免 unused variable 警告
        self.bridge = CvBridge()

    def image_callback(self, msg):
        try:
            # 将ROS图像消息转换为OpenCV格式
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # 定义结构元素
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

            # 定义蓝色的HSV范围
            #lower_blue = np.array([100, 50, 50])
            #upper_blue = np.array([130, 255, 255])

            #lower_blue = np.array([0, 0, 0])
            #upper_blue = np.array([180, 255, 30])

            lower_blue = np.array([0, 100, 100])
            upper_blue = np.array([10, 255, 255])


            # 将图像转换为HSV颜色空间
            hsv_frame = cv.cvtColor(cv_image, cv.COLOR_BGR2HSV)

            # 创建蓝色的掩码
            mask = cv.inRange(hsv_frame, lower_blue, upper_blue)
            mask2 = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
            mask3 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernel)

            # 找出面积最大的区域
            contours, _ = cv.findContours(mask3, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


            maxArea = 0
            maxIndex = 0
            for i, c in enumerate(contours):
                area = cv.contourArea(c)
                if area > maxArea:
                    maxArea = area
                    maxIndex = i

            # 绘制矩形和中心点
            if contours:
                x, y, w, h = cv.boundingRect(contours[maxIndex])
                cv.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                center_x = int(x + w/2)
                center_y = int(y + h/2)
                cv.circle(cv_image, (center_x, center_y), 5, (0, 0, 255), -1)

                # 根据中心点位置进行简单的运动控制反馈
                screen_center = cv_image.shape[1] / 2
                offset = 50
                if center_x < screen_center - offset:
                    print("turn left")
                elif screen_center - offset <= center_x <= screen_center + offset:
                    print("keep")
                elif center_x > screen_center + offset:
                    print("turn right")

            # 显示图像和掩码
            cv.imshow("mask4", mask3)
            cv.imshow("frame", cv_image)
            cv.waitKey(1)

        except CvBridgeError as e:
            print("CvBridgeError:", e)

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

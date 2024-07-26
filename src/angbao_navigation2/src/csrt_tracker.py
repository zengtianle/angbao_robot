import rclpy
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import cv2
from geometry_msgs.msg import Twist
import numpy as np

class ImageConverter:
    def __init__(self):
        self.bridge = CvBridge()
        self.rgb_window = "RGB Image window"
        cv2.namedWindow(self.rgb_window)

        self.select_rect = None
        self.b_renew_roi = False
        self.b_begin_tracking = False
        self.enable_get_depth = False
        self.linear_speed = 0
        self.rotation_speed = 0

        self.k_linear_speed = (0.5 - 0.3) / (5.0 - 1.5)
        self.h_linear_speed = 0.3 - self.k_linear_speed * 1.5

        self.k_rotation_speed = 0.004
        self.h_rotation_speed_left = 1.2
        self.h_rotation_speed_right = 1.36

        self.result = None

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv2.setMouseCallback(self.rgb_window, self.onMouse)

        if not self.b_begin_tracking:
            # Create a fixed size rectangle at the center of the screen
            center_x = cv_image.shape[1] // 2
            center_y = cv_image.shape[0] // 2
            rect_width = 100
            rect_height = 100
            self.select_rect = (center_x - rect_width // 2, center_y - rect_height // 2, rect_width, rect_height)
            self.b_renew_roi = True
            self.b_begin_tracking = True

        if self.b_renew_roi:
            #self.tracker = cv2.TrackerMIL_create()
            self.tracker = cv2.TrackerCSRT_create()
            
            
            bbox = (self.select_rect[0], self.select_rect[1], self.select_rect[2], self.select_rect[3])
            self.tracker.init(cv_image, bbox)
            self.b_renew_roi = False
            self.enable_get_depth = False

        if self.b_begin_tracking:
            success, box = self.tracker.update(cv_image)
            if success:
                p1 = (int(box[0]), int(box[1]))
                p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
                cv2.rectangle(cv_image, p1, p2, (0,255,255), 2, 1)
                self.result = box
                self.enable_get_depth = True

        cv2.imshow(self.rgb_window, cv_image)
        cv2.waitKey(1)

    def depth_callback(self, msg):
        pass

    def camera_info_callback(self, msg):
        pass

    def onMouse(self, event, x, y, flags, param):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('csrt_track')
    ic = ImageConverter()

    image_sub = node.create_subscription(Image, "/camera/color/image_raw", ic.image_callback, 10)
    depth_sub = node.create_subscription(Image, "/camera/aligned_depth_to_color/image_raw", ic.depth_callback, 10)
    camera_info_sub = node.create_subscription(CameraInfo, "/camera/aligned_depth_to_color/camera_info", ic.camera_info_callback, 10)

    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

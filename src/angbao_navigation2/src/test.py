from test2_ros_depth import RealsenseCamera
from angbao_navigation2.msg import CustomDetection

import rclpy
from cv_bridge import CvBridge, CvBridgeError
def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('realsense_camera_node')
    camera = RealsenseCamera(node)
    publisher = node.create_publisher(CustomDetection, 'test_topic', 10)

    try:
        while rclpy.ok():
            # 获取对齐图像帧与相机参数
            color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = camera.get_aligned_images()

            bridge = CvBridge()
            ros_img = bridge.cv2_to_imgmsg(img_color,encoding="bgr8")
                                           
            # 创建 CustomDetection 消息并填充数据
            custom_detection_msg = CustomDetection()
            # 填充图像数据
            custom_detection_msg.image = ros_img

            # 填充锚点数据
            custom_detection_msg.anchors = [1,1,1,1]
            # 填充深度图像数据
            #custom_detection_msg.depth_image = img_depth

            # 发布 CustomDetection 消息
            publisher.publish(custom_detection_msg)
            print("ok")

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

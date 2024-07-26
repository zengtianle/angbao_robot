import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener


def main():
    rclpy.init()
    node = Node("tf_listener_node")  # 创建ROS节点
    tf_buffer = Buffer()
    tf_listener = TransformListener(tf_buffer, node)

    

    try:
        while rclpy.ok():
            print("All TF frames:")
            #print(tf_buffer.all_frames_as_yaml())
            transform = tf_buffer.lookup_transform(
                "test1", "test2",  # 从test1到test2的变换
                rclpy.time.Time())
            print("Transform found: %s", transform)
            rclpy.spin_once(node)
    except KeyboardInterrupt:
        pass
    
    tf_listener.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

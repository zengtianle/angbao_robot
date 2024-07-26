# -*- coding: utf-8 -*-
import pyrealsense2 as rs
import numpy as np
import cv2

class RealsenseCamera:
    def __init__(self):
        # 定义流程pipeline，创建一个管道
        self.pipeline = rs.pipeline()
        # 定义配置config
        self.config = rs.config()
        # 配置depth流
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
        # 配置color流
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
        # streaming流开始
        self.pipe_profile = self.pipeline.start(self.config)
        # align_to 是计划对齐深度帧的流类型
        self.align_to = rs.stream.color
        # rs.align 执行深度帧与其他帧的对齐
        self.align = rs.align(self.align_to)

    # 获取对齐图像帧与相机参数
    def get_aligned_images(self):
        # 等待获取图像帧，获取颜色和深度的框架集
        frames = self.pipeline.wait_for_frames()
        # 获取对齐帧，将深度框与颜色框对齐
        aligned_frames = self.align.process(frames)
        # 获取对齐帧中的的depth帧
        aligned_depth_frame = aligned_frames.get_depth_frame()
        # 获取对齐帧中的的color帧
        aligned_color_frame = aligned_frames.get_color_frame()
        # 获取深度参数（像素坐标系转相机坐标系会用到）
        depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        # 获取相机内参
        color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics
        # RGB图
        img_color = np.asanyarray(aligned_color_frame.get_data())
        # 深度图（默认16位）
        img_depth = np.asanyarray(aligned_depth_frame.get_data())
        return color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame

    # 获取随机点三维坐标
    def get_3d_camera_coordinate(self, depth_pixel, aligned_depth_frame, depth_intrin):
        x = depth_pixel[0]
        y = depth_pixel[1]
        # 获取该像素点对应的深度
        dis = aligned_depth_frame.get_distance(x, y)
        # 获取相机坐标
        camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, depth_pixel, dis)
        return dis, camera_coordinate

if __name__ == "__main__":
    camera = RealsenseCamera()
    while True:
        # 获取对齐图像帧与相机参数
        color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = camera.get_aligned_images()
        # 设置想要获得深度的点的像素坐标，以相机中心点为例
        depth_pixel = [320, 240]
        # 获取对应像素点的三维坐标
        dis, camera_coordinate = camera.get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin)
        print('depth: ', dis)
        print('camera_coordinate: ', camera_coordinate)
        # 在图中标记随机点及其坐标
        cv2.circle(img_color, (depth_pixel[0], depth_pixel[1]), 8, [255, 0, 255], thickness=-1)
        cv2.putText(img_color, "Dis:" + str(dis) + " m", (depth_pixel[0], depth_pixel[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [0, 0, 255])
        cv2.putText(img_color, "X:" + str(camera_coordinate[0]) + " m", (depth_pixel[0], depth_pixel[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [255, 0, 0])
        cv2.putText(img_color, "Y:" + str(camera_coordinate[1]) + " m", (depth_pixel[0], depth_pixel[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [255, 0, 0])
        cv2.putText(img_color, "Z:" + str(camera_coordinate[2]) + " m", (depth_pixel[0], depth_pixel[1] + 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [255, 0, 0])
        # 显示画面
        cv2.imshow('RealSense', img_color)
        key = cv2.waitKey(1)

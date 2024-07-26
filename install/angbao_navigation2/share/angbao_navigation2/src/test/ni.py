import numpy as np

# 假设变换是以旋转平移向量形式表示的
T_camera_to_laser = np.array([
    [7.0842658844480155e-02, 2.1967225457715578e-01,  9.7299815943137014e-01,  -2.4747704487777056e-01],
    [-9.9514252517732238e-01, 8.2411354264238623e-02,  5.3849078655410665e-02,  4.4355727734253239e-02],
    [-6.8356947500214316e-02,  -9.7208665727769539e-01, 2.2444344158635932e-01,  2.0377320541182423e-01],
    [0.0,  0.0,  0.0,  1.0]
])

# 计算逆变换
T_laser_to_camera = np.linalg.inv(T_camera_to_laser)

print("Transformation from laser_frame to camera_link:")
print(T_laser_to_camera)

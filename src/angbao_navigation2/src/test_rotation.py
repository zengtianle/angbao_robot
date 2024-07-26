import numpy as np
from scipy.spatial.transform import Rotation as R

def rotation_matrix_to_quaternion(rot_matrix):
    r = R.from_matrix(rot_matrix)
    quaternion = r.as_quat()
    return quaternion

def quaternion_to_rotation_matrix(quaternion):
    r = R.from_quat(quaternion)
    rotation_matrix = r.as_matrix()
    return rotation_matrix


# 给定的变换矩阵
transform_matrix = [
    7.0842658844480155e-02, 2.1967225457715578e-01, 9.7299815943137014e-01, -2.4747704487777056e-01,
    -9.9514252517732238e-01, 8.2411354264238623e-02, 5.3849078655410665e-02, 4.4355727734253239e-02,
    -6.8356947500214316e-02, -9.7208665727769539e-01, 2.2444344158635932e-01, -2.0377320541182423e-02,
    0., 0., 0., 1.
]
rotation_matrix=np.array([[7.0842658844480155e-02,2.1967225457715578e-01,9.7299815943137014e-01],
                          [-9.9514252517732238e-01,8.2411354264238623e-02,5.3849078655410665e-02],
                          [-6.8356947500214316e-02,-9.7208665727769539e-01,2.2444344158635932e-01]])



# 示例四元数
quaternion = np.array([-0.43703199625252903, 0.4436003983974201, -0.5174914077735109, 0.5868767874722678])

# 将四元数转换为旋转矩阵
rotation_matrix = quaternion_to_rotation_matrix(quaternion)
print("Rotation Matrix:")
print(rotation_matrix)



# 将旋转矩阵转换为四元数
# quaternion = rotation_matrix_to_quaternion(rotation_matrix)
# print("Quaternion:", quaternion)
# print("Rotation Matrix:",rotation_matrix)


